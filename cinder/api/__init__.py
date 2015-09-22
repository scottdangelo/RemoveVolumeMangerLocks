# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
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


from oslo_config import cfg
from oslo_log import log as logging
import paste.urlmap

from cinder.i18n import _LW


CONF = cfg.CONF
LOG = logging.getLogger(__name__)


def root_app_factory(loader, global_conf, **local_conf):
    if CONF.enable_v1_api:
        LOG.warning(_LW('The v1 api is deprecated and will be removed in the '
                        'Liberty release. You should set enable_v1_api=false '
                        'and enable_v2_api=true in your cinder.conf file.'))
    if CONF.enable_v2_api:
        LOG.warning(_LW('The v2 api is deprecated and will be removed in the '
                        'a future release. '))
    return paste.urlmap.urlmap_factory(loader, global_conf, **local_conf)
