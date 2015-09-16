REST API Version History
========================

This documents the changes made to the REST API with every
microversion change. The description for each version should be a
verbose one which has enough information to be suitable for use in
user documentation.

2.0
---
  The 2.0 Cinder API includes all v2 core APIs existing prior to
  the introduction of microversions.  The /v2 URL is used to call
  2.0 APIs, and microversions headers sent to this endpoint are
  ignored.

2.1
---
  This it the initial version of the Cinder API which supports
  microversions.

  A user can specify a header in the API request::

    X-OpenStack-Cinder-API-Version: <version>

  where ``<version>`` is any valid api version for this API.

  If no version is specified then the API will behave as if version 2.0
  was requested.

  The only API change in version 2.1 is versions, i.e.
  GET http://localhost:8786/, which now returns information about
  both 2.0 and 2.x versions and their respective /v2 endpoints.

  All other 2.1 APIs are functionally identical to version 2.0.
