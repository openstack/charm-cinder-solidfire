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
        super().__init__(*args, **kwargs)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.update_status, self._on_update_status)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(
            self.on.storage_backend_relation_changed,
            self._on_storage_backend_changed)

    # @observed
    def _on_install(self, event: InstallEvent):
        self.install_pkgs()
        self.unit.status = ActiveStatus('Unit is ready')

    # @observed
    def _on_update_status(self, event: UpdateStatusEvent):
        expected_status = WaitingStatus('Charm configuration in progress')
        if (self.unit.status == expected_status):
            self.unit.status = ActiveStatus('Unit is ready')

    # @observed
    def _on_config_changed(self, event: ConfigChangedEvent):
        for relation in self.framework.model.relations.get('storage-backend'):
            self._set_relation_data(relation.data[self.unit])
        self.unit.status = ActiveStatus('Unit is ready')

    # @observed
    def _on_storage_backend_changed(self, event: RelationChangedEvent):
        self._set_relation_data(event.relation.data[self.unit])

    def _set_relation_data(self, data) -> None:
        backend_name = self.model.config['volume-backend-name']
        data['backend-name'] = backend_name
        data['subordinate_configuration'] = self._render_config(backend_name)

    def _render_config(self, backend_name) -> str:
        cget = self.model.config.get

        sf_volume_prefix = str(uuid.uuid4()) if cget(
            'sf-volume-prefix') == "UUID" else cget('sf-volume-prefix')

        options = [
            ('volume_driver', VOLUME_DRIVER),
            ('san_ip', cget('san-ip')),
            ('san_login', cget('san-login')),
            ('san_password', cget('san-password')),
            ('sf_account_prefix', cget('sf-account-prefix')),
            ('sf_allow_template_caching',
                cget('sf-allow-template-caching')),
            ('sf_allow_tenant_qos', cget('sf-allow-tenant-qos')),
            ('sf_api_port', cget('sf-api-port')),
            ('sf_emulate_512', cget('sf-emulate-512')),
            ('sf_enable_vag', cget('sf-enable-vag')),
            ('sf_enable_volume_mapping', cget('sf-enable-volume-mapping')),
            ('sf_svip', cget('sf-svip')),
            ('sf_template_account_name', cget('sf-template-account-name')),
            ('sf_volume_prefix', sf_volume_prefix)
        ]
        return json.dumps({
            "cinder": {
                "/etc/cinder/cinder.conf": {
                    "sections": {backend_name: options}
                }
            }
        })


if __name__ == '__main__':
    main(CinderSolidfireCharm)
