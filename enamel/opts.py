# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg


def list_opts():
    return [
        ("api", (
            cfg.PortOpt('bind_port',
                        default=5050,
                        help='The port for the Enamel API server.'),
            cfg.StrOpt('bind_address',
                       default='0.0.0.0',
                       help='The listen IP for the Enamel API server.'),
            cfg.StrOpt('auth_strategy',
                       default='keystone',
                       help='The authentication strategy. '
                            'Set to None to disable auth.'),
        )),
        ("task-processor", (
            cfg.PortOpt(
                'bind_port',
                default=5050,
                help='The port for the Enamel task processor worker.'),
            cfg.StrOpt(
                'bind_address',
                default='0.0.0.0',
                help='The listen IP for the Enamel task processor worker.'),
            cfg.StrOpt(
                'pidfile',
                default='/var/run/enamel-task-processor.pid',
                help='The path to the pidfile for the task processor daemon.'),
        )),
    ]
