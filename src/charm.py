#! /usr/bin/env python3

# Copyright 2021 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import uuid
import logging

from ops.main import main
from ops_openstack.plugins.classes import BaseCinderCharm

logger = logging.getLogger(__name__)

VOLUME_DRIVER = 'cinder.volume.drivers.solidfire.SolidFireDriver'


class CinderSolidfireCharm(BaseCinderCharm):

    PACKAGES = ['cinder-common']
    # Overriden from the parent. May be set depending on the charm's properties
    stateless = False
    active_active = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cinder_configuration(self, charm_config) -> 'list[tuple]':
        """Return the configuration to be set by the principal"""
        cget = charm_config.get

        sf_volume_prefix = str(uuid.uuid4()) if cget(
            'volume-prefix') == "UUID" else cget('volume-prefix')

        raw_options = [
            ('volume_driver', VOLUME_DRIVER),
            ('san_ip', cget('san-ip')),
            ('san_login', cget('san-login')),
            ('san_password', cget('san-password')),
            ('sf_account_prefix', cget('account-prefix')),
            ('sf_allow_template_caching',
                cget('allow-template-caching')),
            ('sf_allow_tenant_qos', cget('allow-tenant-qos')),
            ('sf_api_port', cget('api-port')),
            ('sf_emulate_512', cget('emulate-512')),
            ('sf_enable_vag', cget('enable-vag')),
            ('sf_enable_volume_mapping', cget('enable-volume-mapping')),
            ('sf_svip', cget('svip')),
            ('sf_template_account_name', cget('template-account-name')),
            ('sf_volume_prefix', sf_volume_prefix)
        ]
        options = [(x, y) for x, y in raw_options if y]
        return options


if __name__ == '__main__':
    main(CinderSolidfireCharm)
