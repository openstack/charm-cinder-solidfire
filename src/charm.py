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


from ops_openstack.core import OSBaseCharm
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus


class CinderSolidfireCharm(OSBaseCharm):

    _stored = StoredState()
    PACKAGES = ['cinder-common']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We listen to the following events:
        # - Installation: Just to set the charm status
        # - Configuration changes: Rewrite the cinder.conf file and inform
        #   other charms of the changes
        # - Backend storage join/change: Inform the other charm of what the
        #   configuration is and the backend name.
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.config_changed, self._on_config)
        self.framework.observe(
            self.on.storage_backend_relation_joined,
            self._on_storage_backend)
        self.framework.observe(
            self.on.storage_backend_relation_changed,
            self._on_storage_backend)

    def _on_install(self, _):
        self.install_pkgs()
        self.unit.status = ActiveStatus('Unit is ready')

    def _render_config(self, config, app_name):
        # Generate the JSON with the updated configuration.
        volume_driver = ''
        options = [
            ('volume_driver', volume_driver),
        ]
        return json.dumps({
            "cinder": {
                "/etc/cinder/cinder.confg": {
                    "sections": {app_name: options}
                }
            }
        })

    def _set_data(self, data, config, app_name):
        # Inform another charm of the backend name and our configuration.
        data['backend-name'] = config['volume-backend-name'] or app_name
        data['subordinate_configuration'] = self._render_config(
            config, app_name)

    def _on_config(self, event):
        config = dict(self.framework.model.config)
        rel = self.framework.model.relations.get('storage-backend')[0]
        app_name = self.framework.model.app.name
        for unit in self.framework.model.get_relation('storage-backend').units:
            self._set_data(rel.data[self.unit], config, app_name)
        self.unit.status = ActiveStatus('Unit is ready')

    def _on_storage_backend(self, event):
        self._set_data(
            event.relation.data[self.unit],
            self.framework.model.config,
            self.framework.model.app.name)


if __name__ == '__main__':
    main(CinderSolidfireCharm)
