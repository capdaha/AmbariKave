##############################################################################
#
# Copyright 2016 KPMG Advisory N.V. (unless otherwise stated)
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
import base
import unittest


class TestBlueprint(base.LDTest):

    def runTest(self):
        """
        The remote_blueprint test ups a dev machine and submits a blueprint to it.
        It monitors the status of the request corresponding to the blueprint
        """
        # create remote machine
        import os
        import sys
        import json

        lD = self.pre_check()
        deploy_dir = os.path.realpath(os.path.dirname(lD.__file__) + '/../')
        af = os.path.dirname(__file__) + "/blueprints/default.aws.json"
        bp = os.path.dirname(__file__) + "/blueprints/" + self.service + ".blueprint.json"
        cf = os.path.dirname(__file__) + "/blueprints/default.cluster.json"
        if not os.path.exists(bp):
            raise ValueError("No blueprint with which to install " + self.service)
        self.verify_blueprint(af, bp, cf)
        ambari, iid = self.deploy_dev("c4.2xlarge")  # 2xlarge needed for single node hadoop!
        # clean the existing blueprint ready for re-install
        self.pull(ambari)
        self.resetambari(ambari)
        self.deploy_blueprint(ambari, bp, cf)
        return self.check(ambari)


#####
# If you need to update this, go to the machine where this test fialed, and run ./AmbariKave/dev/scan.sh
#####
__kavelanding_plain__ = """Welcome to your KAVE
==================
* 'default' cluster
|--* Servers
|  |--* Ambari <a href='http://ambari:8080'>admin</a>
|  |--* Jenkins <a href='http://ambari:8888'>jenkins</a>
|  |--* Metrics <a href='http://ambari:3000'>grafana</a>
|  |--* Metrics collector (['ambari.kave.io'])
|  |--* Zookeeper (['ambari.kave.io'])
|
|--* Clients
|  |--* ambari.kave.io ['kavelanding', 'metrics_monitor', 'zookeeper_client']"""


#####
# If you need to update this, go to the machine where this test failed, and run ./AmbariKave/dev/scan.sh html
#####
__kavelanding_html__ = """<h3><font size=5px>'default' cluster</font></h3>
<b>Servers</b><p><ul>
  <li>Ambari <a href='http://ambari:8080'>admin</a></li>
  <li>Jenkins <a href='http://ambari:8888'>jenkins</a></li>
  <li>Metrics <a href='http://ambari:3000'>grafana</a></li>
  <li>Metrics collector (['ambari.kave.io'])</li>
  <li>Zookeeper (['ambari.kave.io'])</li>
</ul><p><b>Clients</b><p><ul>
  <li>ambari.kave.io ['kavelanding', 'metrics_monitor', 'zookeeper_client']</li>
</ul>"""


class TestServiceKaveLanding(TestBlueprint):

    def check(self, ambari):
        super(TestServiceKaveLanding, self).check(ambari)
        ppp = ambari.run("./[a,A]mbari[k,K]ave/dev/scan.sh")
        pph = ambari.run("./[a,A]mbari[k,K]ave/dev/scan.sh localhost html")
        self.assertTrue(nowhite(__kavelanding_plain__) == nowhite(ppp),
                        "Incorrect response from KaveLanding, scan.sh \n" + __kavelanding_plain__ +
                        "\n-----------\nnot equal to\n-------\n" + ppp)
        self.assertTrue(nowhite(__kavelanding_html__) in nowhite(pph),
                        "Incorrect response from KaveLanding, scan.sh" + __kavelanding_html__ + "\n-----------\nnot "
                                                                                                "equal to\n-------\n"
                        + pph)
        pph2 = ambari.run("curl --retry 5  -X GET http://localhost/", exit=False)
        self.assertTrue(nowhite(__kavelanding_html__) in nowhite(pph2), "KaveLanding page is incomplete")


class TestServiceFreeIPA(TestBlueprint):

    def check(self, ambari):
        super(TestServiceFreeIPA, self).check(ambari)
        # Check kerberos
        import subprocess as sub
        import os
        pwd = ambari.run("cat admin-password")
        proc = sub.Popen(ambari.sshcmd() + ['kinit admin'], shell=False,
                         stdout=sub.PIPE, stderr=sub.PIPE, stdin=sub.PIPE)
        output, err = proc.communicate(input=pwd + '\n')
        self.assertFalse(proc.returncode, "Failed to kinit admin on this node "
                         + ' '.join(ambari.sshcmd())
                         + output + " " + err
                         )
        ambari.cp(os.path.dirname(__file__) + '/kerberostest.csv', 'kerberostest.csv')
        ambari.run("./createkeytabs.py ./kerberostest.csv")
        # check port number patching still applies correctly
        ambari.run("python "
                   "/var/lib/ambari-server/resources/stacks/HDP/*.KAVE/services/FREEIPA/package/scripts/sed_ports.py"
                   " --test /etc/kave/portchanges_static.json --debug")
        ambari.run("python "
                   "/var/lib/ambari-server/resources/stacks/HDP/*.KAVE/services/FREEIPA/package/scripts/sed_ports.py"
                   " --test /etc/kave/portchanges_new.json --debug")


if __name__ == "__main__":
    import sys

    verbose = False
    branch = "__local__"
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv = [s for s in sys.argv if s != "--verbose"]
    if len(sys.argv) < 2:
        raise KeyError("You must specify which service to test")
    if "--branch" in sys.argv:
        branch = "__service__"
        sys.argv = [s for s in sys.argv if s != "--branch"]
    if "--this-branch" in sys.argv:
        branch = "__local__"
        sys.argv = [s for s in sys.argv if s != "--this-branch"]
    service = sys.argv[1]
    test = TestBlueprint()
    if service == "KAVELANDING":
        test = TestServiceKaveLanding()
    if service == "FREEIPA":
        test = TestServiceFreeIPA()
    test.service = service
    test.debug = verbose
    test.branch = branch
    test.checklist = []
    if len(sys.argv) > 2:
        test.checklist = sys.argv[2:]
    suite = unittest.TestSuite()
    suite.addTest(test)
    base.run(suite)
