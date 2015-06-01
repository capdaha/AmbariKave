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
import base
import unittest


class TestServiceBlueprint(base.LDTest):
    def runTest(self):
        # create remote machine
        import os
        import sys

        lD = self.preCheck()
        deploy_dir = os.path.realpath(os.path.dirname(lD.__file__) + '/../')
        if not os.path.exists(os.path.dirname(__file__) + "/blueprints/" + self.service + ".blueprint.json"):
            raise ValueError("No blueprint with which to install " + self.service)
        if self.service not in [s for s, d in base.findServices()]:
            raise ValueError(
                "This test can only work for blueprints where the name of the blueprint matches a known service. Else "
                "try remote_blueprint.py")
        ambari,iid = self.deployDev()
        #clean the existing blueprint ready for re-install
        self.resetambari(ambari)
        self.deployBlueprint(ambari, os.path.dirname(__file__) + "/blueprints/" + self.service + ".blueprint.json",
                             os.path.dirname(__file__) + "/blueprints/default.cluster.json")
        #import time
        #time.sleep(15)
        #wait for the install and then check if the directories etc. are there
        self.waitForService(ambari)
        self.check(ambari)


__kavelanding_plain__ = """Welcome to your KAVE
==================
* 'default' cluster
|--* Servers
|  |--* Ambari <a href='http://ambari:8080'>admin</a>
|  |--* Nagios <a href='http://ambari:80/nagios'>alerts</a>
|  |--* Jenkins <a href='http://ambari:8888'>jenkins</a>
|  |--* Ganglia <a href='http://ambari:80/ganglia'>monitor</a>
|
|--* Clients
|  |--* ambari.kave.io ['GANGLIA_MONITOR', 'KAVELANDING']"""

__kavelanding_html__ = """<h3><font size=5px>'default' cluster</font></h3>
<b>Servers</b><p><ul>
  <li>Ambari <a href='http://ambari:8080'>admin</a></li>
  <li>Nagios <a href='http://ambari:80/nagios'>alerts</a></li>
  <li>Jenkins <a href='http://ambari:8888'>jenkins</a></li>
  <li>Ganglia <a href='http://ambari:80/ganglia'>monitor</a></li>
</ul><p><b>Clients</b><p><ul>
  <li>ambari.kave.io ['GANGLIA_MONITOR', 'KAVELANDING']</li>
</ul>"""


def nowhite(astring):
    """
    return a string with no whitespace
    """
    return ''.join(astring.split())


class TestServiceKaveLanding(TestServiceBlueprint):
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
        pph2 = ambari.run("curl -X GET http://localhost/", exit=False)
        self.assertTrue(nowhite(__kavelanding_html__) in nowhite(pph2), "KaveLanding page is incomplete")


if __name__ == "__main__":
    import sys

    verbose = False
    branch = "__local__"
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv = [s for s in sys.argv if s != "--verbose"]
    if "--branch" in sys.argv:
        branch = "__service__"
        sys.argv = [s for s in sys.argv if s != "--branch"]
    if "--this-branch" in sys.argv:
        branch = "__local__"
        sys.argv = [s for s in sys.argv if s != "--this-branch"]
    if len(sys.argv) < 2:
        raise KeyError("You must specify which service to test")
    service = sys.argv[1]
    test = TestServiceBlueprint()
    if service == "KAVELANDING":
        test = TestServiceKaveLanding()
    test.service = service
    test.debug = verbose
    test.branch = branch
    test.checklist = []
    if len(sys.argv) > 2:
        test.checklist = sys.argv[2:]
    suite = unittest.TestSuite()
    suite.addTest(test)
    base.run(suite)