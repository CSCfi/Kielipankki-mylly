# TOOL hfst-compose.py: "Intersection"
# (Intersect HFST transducers. Match archives pairwise, or broadcast the second archive.)
# INPUT input1.hfst TYPE GENERIC
# INPUT input2.hfst TYPE GENERIC
# OUTPUT output.hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER SymbolHarm
#     TYPE [yes: "do harmonize symbols",
#           no: "do not harmonize symbols"]
#     DEFAULT yes
#     (do not expand '?' symbols, maybe)
# PARAMETER FlagHarm
#     TYPE [yes: "do harmonize flags",
#           no: "do not harmonize flags"]
#     DEFAULT no
#     (something about flags, maybe)
# PARAMETER Version TYPE [v_3_12_1: "3.12.1", v_3_11_0: "3.11.0", v_3_9_0: "3.9.0", v_3_8_3: "3.8.3"] DEFAULT v_3_12_1 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

names.output('output.hfst', names.replace('input1.hfst', '-i.hfst'))

hfst.setenv(Version)

symbolharm = dict(yes = [], no = ['--do-not-harmonize'])[SymbolHarm]
flagharm = dict(yes = ['--harmonize-flags'], no = [])[FlagHarm]

with Popen(['hfst-intersect', '-o', 'output.hfst']
           + symbolharm
           + flagharm
           + ['input1.hfst', 'input2.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'output.hfst',
            version = 'hfst-intersect' if VersionLog == 'produce' else None)
