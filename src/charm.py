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


import json
import uuid
import logging

from ops.charm import (ConfigChangedEvent, InstallEvent, RelationChangedEvent,
                       UpdateStatusEvent)
from ops_openstack.core import OSBaseCharm
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, WaitingStatus

logger = logging.getLogger(__name__)

VOLUME_DRIVER = 'cinder.volume.drivers.solidfire.SolidFireDriver'


class CinderSolidfireCharm(OSBaseCharm):

    _stored = StoredState()
    PACKAGES = ['cinder-common']

    def __init__(self, *args, **kwargs):
        """Set observables to watch"""
        super().__init__(*args, **kwargs)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.update_status, self._on_update_status)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(
            self.on.storage_backend_relation_changed,
            self._on_storage_backend_changed)

    def _on_install(self, event: InstallEvent):
        """Install ubuntu packages"""
        self.install_pkgs()
        self.unit.status = ActiveStatus('Unit is ready')

    def _on_update_status(self, event: UpdateStatusEvent):
        """Mantain active status if everything is okay"""
        expected_status = WaitingStatus('Charm configuration in progress')
        if (self.unit.status == expected_status):
            self.unit.status = ActiveStatus('Unit is ready')

    def _on_config_changed(self, event: ConfigChangedEvent):
        """Update information to main charm on config change"""
        for relation in self.framework.model.relations.get('storage-backend'):
            self._set_relation_data(relation.data[self.unit])
        self.unit.status = ActiveStatus('Unit is ready')

    def _on_storage_backend_changed(self, event: RelationChangedEvent):
        """Send information to main charm on backend relation event"""
        self._set_relation_data(event.relation.data[self.unit])

    def _set_relation_data(self, data) -> None:
        """Send information to main charm through subordinate relation"""
        backend_name = self.model.config['volume-backend-name']
        data['backend-name'] = backend_name
        data['subordinate_configuration'] = self._render_config(backend_name)

    def _render_config(self, backend_name) -> str:
        """Generate backend configuration for cinder.conf"""
        cget = self.model.config.get

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

        return json.dumps({
            "cinder": {
                "/etc/cinder/cinder.conf": {
                    "sections": {backend_name: options}
                }
            }
        })


if __name__ == '__main__':
    main(CinderSolidfireCharm)
