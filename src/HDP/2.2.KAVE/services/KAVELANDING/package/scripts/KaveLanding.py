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
from kavecommon import ApacheScript


class KaveLanding(ApacheScript):
    def install(self, env):
        print "installing KaveLanding"
        import params
        import kavecommon as kc
        super(KaveLanding,self).install(env)
        #needs installation of bower ...
        Execute('yum -y groupinstall "Development Tools"')
        kc.copyCacheOrRepo('nodejs-setup.sh')
        #Execute('wget https://rpm.nodesource.com/setup')
        Execute('bash nodejs-setup.sh')
        Package('nodejs')
        #Execute('yum install -y nodejs')
        Execute('npm install -g bower')
        Execute('echo n | bower --allow-root --help')
        Execute('bower install bootstrap --allow-root')
        import os
        Execute('cp '+os.path.dirname(__file__)+'/KAVE-logo-thin.png '+params.www_folder+'/')
        Execute('chmod 0644 '+params.www_folder+'/KAVE-logo-thin.png')
        self.configure(env)
        #self.start(env)
        super(KaveLanding, self).install(env)
        #needs installation of bower ...
        Execute('yum -y groupinstall "Development Tools"')
        kc.copyCacheOrRepo('nodejs-setup.sh')
        #Execute('wget https://rpm.nodesource.com/setup')
        Execute('bash nodejs-setup.sh')
        Package('nodejs')
        #Execute('yum install -y nodejs')
        Execute('npm install -g bower')
        Execute('echo n | bower --allow-root --help')
        Execute('bower install bootstrap --allow-root')
        self.configure(env)
        #self.start(env)

    def configure(self, env):
        import params, os
        import kavecommon as kc
        env.set_params(params)
        self.writeHTML(env)
        super(KaveLanding, self).configure(env)

    def writeHTML(self,env):
        import params
        import kavecommon as kc
        env.set_params(params)
        if os.path.exists(params.www_folder+'/index.html'):
            os.remove(params.www_folder+'/index.html')
        File(params.www_folder+'/index.html',
           content = Template("kavelanding.html.j2"),
           mode = 0644
           )
        File(params.www_folder+'/bootstrap.min.css',
           content = Template("bootstrap.min.css"),
           mode = 0644
           )
        File(params.www_folder+'/LICENSE',
           content = Template("LICENSE"),
           mode = 0644
           )
        File(params.www_folder+'/LICENCE-DOCUMENTATION-IMAGE-SUBCLAUSE',
           content = Template("LICENCE-DOCUMENTATION-IMAGE-SUBCLAUSE"),
           mode = 0644
           )
        File(params.www_folder+'/NOTICE',
           content = Template("NOTICE"),
           mode = 0644
           )
        # HINT: Use this in future: http://jinja.pocoo.org/docs/dev/templates/
        import libScan as ls
        ls.ambari_user=params.AMBARI_ADMIN
        ls.ambari_password=params.AMBARI_ADMIN_PASS
        cluster_service_host, cluster_host_service, cluster_service_link=ls.collect_config_data(params.AMBARI_SHORT_HOST)
        bodyhtml=ls.pretty_print(cluster_service_host, cluster_host_service, cluster_service_link, format="html")
        #HINT: this can be replaced by the correct template language in future
        HUE_LINK_IF_KNOWN=""
        all_links=[]
        for cluster in cluster_service_link:
            if "HUE_SERVER" in cluster_service_link[cluster]:
                HUE_LINK_IF_KNOWN="<li>"+cluster_service_link[cluster]["HUE_SERVER"][0]+"</li>"
        for cluster in cluster_service_link:
            for service in cluster_service_link[cluster]:
               all_links=all_links+["<li>"+l+"</li>" for l in cluster_service_link[cluster][service]]
        f=open(params.www_folder+'/index.html')
        content=f.read()
        f.close()
        f=open(params.www_folder+'/index.html','w')
        if len(cluster_service_link.keys()) == 1:
            content=content.replace("<title>KAVE:","<title>"+cluster_service_link.keys()[0]+"-KAVE:")
        f.write(content.replace("THEPAGE!!",bodyhtml).replace("HUE_LINK_IF_KNOWN",HUE_LINK_IF_KNOWN).replace("ALL_OTHER_LINKS","\n".join(all_links)))
        f.close()
        kc.chownR(params.www_folder,"apache")

    def start(self, env):
        #print "start apache"
        #Execute('service httpd start')
        self.configure(env)
        super(KaveLanding, self).start(env)

    def stop(self, env):
        #print "stop apache.."
        import params

        super(KaveLanding, self).stop(env)
        if os.path.exists(params.www_folder + '/index.html'):
            os.remove(params.www_folder + '/index.html')


    def status(self, env):
        #print "checking status..."
        super(KaveLanding, self).status(env)
        import params

        return os.path.exists(params.www_folder + '/index.html')


if __name__ == "__main__":
    KaveLanding().execute()