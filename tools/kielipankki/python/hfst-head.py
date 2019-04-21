# TOOL hfst-head.py: "Head of an archive"
# (Take a number of transducers from the head of an archive, or take the rest.)
# INPUT input.hfst: "Transducers" TYPE GENERIC
#     (An HFST transducer archive)
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
from lib_names2 import base, name
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

name('output.hfst', base('input.hfst', '*.hfst') + 'head-{}'.format(Number),
     ext = 'hfst')

hfst.setenv(Version)

with Popen(['hfst-head', '-o', 'output.hfst',
            '-n', str(Number),
            'input.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'output.hfst',
            version = 'hfst-head' if VersionLog == 'produce' else None)
