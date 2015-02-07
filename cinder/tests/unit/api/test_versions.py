# Copyright 2015 Clinton Knight
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import ddt
import mock
from oslo_serialization import jsonutils

from cinder.api.openstack import api_version_request
from cinder.api.openstack import wsgi
from cinder.api.v1 import router
from cinder.api import versions
from cinder import test
from cinder.tests.unit.api import fakes


version_header_name = 'X-OpenStack-Cinder-API-Version'


@ddt.ddt
class VersionsControllerTestCase(test.TestCase):

    def setUp(self):
        super(VersionsControllerTestCase, self).setUp()
        self.wsgi_apps = (versions.VersionsRouter(), router.APIRouter())

    @ddt.data('2.0', '2.1')
    def test_versions_root(self, version):
        req = fakes.HTTPRequest.blank('/', base_url='http://localhost')
        req.method = 'GET'
        req.content_type = 'application/json'

        response = req.get_response(versions.VersionsRouter())
        self.assertEqual(300, response.status_int)
        body = jsonutils.loads(response.body)
        version_list = body['versions']

        ids = [v['id'] for v in version_list]
        self.assertEqual({'v2.0', 'v2.1'}, set(ids))

        v2 = [v for v in version_list if v['id'] == 'v2.0'][0]
        self.assertEqual('', v2.get('min_version'))
        self.assertEqual('', v2.get('version'))

        v2_1 = [v for v in version_list if v['id'] == 'v2.1'][0]
        self.assertEqual(api_version_request._MAX_API_VERSION,
                         v2_1.get('version'))
        self.assertEqual(api_version_request._MIN_API_VERSION,
                         v2_1.get('min_version'))

    @ddt.data('2.0')
    def test_versions_v2(self, version):
        req = fakes.HTTPRequest.blank('/', base_url='http://localhost/v2')
        req.method = 'GET'
        req.content_type = 'application/json'
        req.headers = {version_header_name: version}

        response = req.get_response(router.APIRouter())
        self.assertEqual(200, response.status_int)
        body = jsonutils.loads(response.body)
        version_list = body['versions']

        ids = [v['id'] for v in version_list]
        self.assertEqual({'v2.0'}, set(ids))
        self.assertEqual('2.0', response.headers[version_header_name])
        self.assertEqual(version, response.headers[version_header_name])
        self.assertEqual(version_header_name, response.headers['Vary'])

        self.assertEqual('', version_list[0].get('min_version'))
        self.assertEqual('', version_list[0].get('version'))

    @ddt.data('2.1')
    def test_versions_v2_1(self, version):
        req = fakes.HTTPRequest.blank('/', base_url='http://localhost/v2')
        req.method = 'GET'
        req.content_type = 'application/json'
        req.headers = {version_header_name: version}

        response = req.get_response(router.APIRouter())
        self.assertEqual(200, response.status_int)
        body = jsonutils.loads(response.body)
        version_list = body['versions']

        ids = [v['id'] for v in version_list]
        self.assertEqual({'v2.1'}, set(ids))
        self.assertEqual('2.1', response.headers[version_header_name])
        self.assertEqual(version, response.headers[version_header_name])
        self.assertEqual(version_header_name, response.headers['Vary'])

        self.assertEqual(api_version_request._MAX_API_VERSION,
                         version_list[0].get('version'))
        self.assertEqual(api_version_request._MIN_API_VERSION,
                         version_list[0].get('min_version'))

    def test_versions_version_invalid(self):
        req = fakes.HTTPRequest.blank('/', base_url='http://localhost/v2')
        req.method = 'GET'
        req.content_type = 'application/json'
        req.headers = {version_header_name: '2.0.1'}

        for app in self.wsgi_apps:
            response = req.get_response(app)

            self.assertEqual(400, response.status_int)

    def test_versions_version_not_found(self):
        api_version_request_8_0 = api_version_request.APIVersionRequest('8.0')
        self.mock_object(api_version_request,
                         'max_api_version',
                         mock.Mock(return_value=api_version_request_3_0))

        class Controller(wsgi.Controller):

            @wsgi.Controller.api_version('2.1', '2.1')
            def index(self, req):
                return 'off'

        req = fakes.HTTPRequest.blank('/tests', base_url='http://localhost/v2')
        req.headers = {version_header_name: '2.5'}
        app = fakes.TestRouter(Controller())

        response = req.get_response(app)

        self.assertEqual(404, response.status_int)

    def test_versions_version_not_acceptable(self):
        req = fakes.HTTPRequest.blank('/', base_url='http://localhost/v2')
        req.method = 'GET'
        req.content_type = 'application/json'
        req.headers = {version_header_name: '3.0'}

        response = req.get_response(router.APIRouter())

        self.assertEqual(406, response.status_int)
        self.assertEqual('3.0', response.headers[version_header_name])
        self.assertEqual(version_header_name, response.headers['Vary'])
