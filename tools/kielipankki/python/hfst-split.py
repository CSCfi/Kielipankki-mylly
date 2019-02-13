# TOOL hfst-split.py: "Split an archive"
# (Split an HFST archive into individual transducers.)
# INPUT input.hfst TYPE GENERIC
# OUTPUT output-{...}-hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Version TYPE [v_3_14_0: "3.14.0"] DEFAULT v_3_14_0 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# RUNTIME python3

# Note that output-{...}-hfst is not a typo. Hope this works out.

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_hfst as hfst

import glob, os, shutil
from subprocess import Popen

hfst.setenv(Version)

with Popen(['hfst-split', '--prefix', 'output-', '--extension', '-hfst',
            'input.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

for oh in glob.glob('output-*-hfst'):
    o, N, h = oh.split('-')
    names.output(oh, names.replace('input.hfst', '-{}.hfst'.format(N)))

hfst.finish(version = 'hfst-split' if VersionLog == 'produce' else None)
