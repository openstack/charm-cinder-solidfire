# Copyright 2016 Canonical Ltd
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

import unittest
from src.charm import CinderSolidfireCharm
from ops.model import ActiveStatus
from ops.testing import Harness


class TestCinderSolidfireCharm(unittest.TestCase):

    def setUp(self):
        self.harness = Harness(CinderSolidfireCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()
        self.harness.set_leader(True)
        backend = self.harness.add_relation('storage-backend', 'cinder')
        self.harness.update_config({'volume-backend-name': 'test'})
        self.harness.add_relation_unit(backend, 'cinder/0')

    def test_cinder_base(self):
        self.assertEqual(
            self.harness.framework.model.app.name,
            'cinder-solidfire')
        # Test that charm is active upon installation.
        self.harness.update_config({})
        self.assertTrue(isinstance(
            self.harness.model.unit.status, ActiveStatus))

    def test_cinder_configuration(self):
        # Add check here that configuration is as expected.
        pass
