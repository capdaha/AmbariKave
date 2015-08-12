##############################################################################
#
# Copyright 2015 KPMG N.V. (unless otherwise stated)
#
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
##############################################################################
import status_params

from resource_management import *
from ambari_commons.os_check import OSCheck

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

sonarqube_supported_plugins = ['sonar-python-plugin-1.5.jar']

sonarqube_install_directory = default('configurations/sonarqube/sonarqube_install_directory', '/opt/sonarqube')
sonarqube_runner_install_directory = default('configurations/sonarqube/sonarqube_runner_install_directory',
                                             '/opt/sonarqube_runner')
sonarqube_plugins = set()
for plugin in default('configurations/sonarqube/sonarqube_plugins', 'sonar-python-plugin-1.5.jar').split(','):
    if plugin == '':
        continue
    elif plugin in sonarqube_supported_plugins:
        sonarqube_plugins.add(plugin)
    else:
        print 'Ignoring unsupported plugin: %s' % plugin

sonar_host = default('configurations/sonarqube/sonar_host', 'localhost')
sonar_web_port = default('configurations/sonarqube/sonar_web_port', '5051')

sonar_database_url = default('configurations/sonarqube/sonar_database_url', 'localhost')
sonar_database_user_name = default('configurations/sonarqube/sonar_database_user_name', 'sonarqube')
sonar_database_user_passwd = config['configurations']['sonarqube']['sonar_database_user_passwd']

if not sonar_database_user_passwd:
    raise Exception('sonar_database_user_passwd needs to be set')

mysql_adduser_path = format("{tmp_dir}/addMysqlUser.sh")
mysql_deluser_path = format("{tmp_dir}/removeMysqlUser.sh")

daemon_name = status_params.daemon_name

if OSCheck.is_ubuntu_family():
    mysql_configname = '/etc/mysql/my.cnf'
else:
    mysql_configname = '/etc/my.cnf'
