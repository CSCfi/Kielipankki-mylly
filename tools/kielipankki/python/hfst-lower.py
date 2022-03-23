# TOOL hfst-lower.py: "Lower projection"
# (Project to the lower level of the transducer.)
# INPUT input.hfst: "Transducers" TYPE GENERIC
# OUTPUT output.hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Version TYPE [v_3_14_0: "3.14.0"] DEFAULT v_3_14_0 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

name('output.hfst', base('input.hfst', '*.hfst'),
     ins = 'lower',
     ext = 'hfst')

hfst.setenv(Version)

with Popen(['hfst-project', '-o', 'output.hfst',
            '--project', 'lower',
            'input.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'output.hfst',
            version = 'hfst-project' if VersionLog == 'produce' else None)
