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
import os

from resource_management import *
import kavecommon as kc


class Hue(Script):
    conf_dirs = ["/etc/hue/conf.empty", "/etc/hue/conf.d", "/etc/hue/conf"]

    def install(self, env):
        import params

        env.set_params(params)
        self.install_packages(env)
        self.configure(env)

    def configure(self, env):
        import params, os
        import kavecommon as kc

        env.set_params(params)
        Execute('chkconfig --levels 235 hue on')
        for dir in self.conf_dirs:
            if not os.path.exists(dir):
                continue
            dir = os.path.realpath(dir)
            File(dir + '/hue.ini', content=Template("hue.ini.j2"), mode=0755)
            File(dir + '/hue_httpd.conf', content=Template("hue_httpd.conf.j2"), mode=0755)
            Execute('chmod -R 755 ' + dir)

    def start(self, env):
        Execute("service hue start")

    def stop(self, env):
        Execute('service hue stop')


    def status(self, env):
        print Execute('service hue status')


if __name__ == "__main__":
    Hue().execute()