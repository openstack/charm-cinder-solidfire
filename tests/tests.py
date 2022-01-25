from zaza.openstack.charm_tests.cinder_backend.tests import CinderBackendTest
from os import environ


class CinderSolidfireTest(CinderBackendTest):
    """Encapsulate cinder-solidfire tests."""

    backend_name = 'cinder-solidfire'

    expected_config_content = {
        'cinder-solidfire': {
            'volume_driver':
            ['cinder.volume.drivers.solidfire.SolidFireDriver'],
            'san_ip': environ['TEST_SOLIDFIRE_SAN_IP'],
            'san_login': environ['TEST_SOLIDFIRE_SAN_USERNAME'],
            'san_password': environ['TEST_SOLIDFIRE_SAN_PASSWORD']
        }}
