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
import deploylib
import kclib
import servicesh
import scan
import license
import pyfilenames
import testversion
import ipaportsed
import testpythonimport
import verifyxml
import checkpep8
import pep8functions
import pep8variables
import jsonbpchecks
import repoimports
import testresourcewizard
import base
import checkdistkclib
import sys

mods = [testresourcewizard, checkpep8, testpythonimport, testversion,
        pep8functions, deploylib, kclib, servicesh, scan, license, repoimports,
        pyfilenames, pep8variables, jsonbpchecks, verifyxml,
        ipaportsed, checkdistkclib]

if __name__ == "__main__":
    # Repo imports does not work on jenkins, no idea why ... perhaps memory usage?
    if '--jenkins' in sys.argv:
        mods = [m for m in mods if m not in [repoimports]]
    base.parallel(mods)
