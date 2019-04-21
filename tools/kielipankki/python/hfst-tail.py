# TOOL hfst-tail.py: "Tail of an archive"
# (Take a number of transducers from the tail of an archive, or take the rest.)
# INPUT input.hfst TYPE GENERIC
# OUTPUT output.hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Number
#     TYPE INTEGER
#     DEFAULT 1
#     (The number of transducers to take, or drop if negative)
# PARAMETER Version TYPE [v_3_14_0: "3.14.0"] DEFAULT v_3_14_0 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name # TODO
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

names.output('output.hfst', names.replace('input.hfst', '-t{}.hfst'.format(Number)))

hfst.setenv(Version)

with Popen(['hfst-tail', '-o', 'output.hfst',
            '-n', str(Number),
            'input.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'tail.hfst',
            version = 'hfst-head' if VersionLog == 'produce' else None)
