# TOOL hfst-concatenate.py: "Concatenation"
# (Concatenate HFST transducers. Match archives pairwise, or broadcast the second archive.)
# INPUT input1.hfst: "First transducers" TYPE GENERIC
#     (An HFST transducer archive)
# INPUT input2.hfst: "Second transducers" TYPE GENERIC
#     (An HFST transducer archive)
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
# PARAMETER Version TYPE [v_3_14_0: "3.14.0"] DEFAULT v_3_14_0 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# IMAGE comp-16.04-mylly
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

name('output.hfst', base('input1.hfst', '*.hfst'),
     ins = 'c',
     ext = 'hfst')

hfst.setenv(Version)

symbolharm = dict(yes = [], no = ['--do-not-harmonize'])[SymbolHarm]
flagharm = dict(yes = ['--harmonize-flags'], no = [])[FlagHarm]

with Popen(['hfst-concatenate', '-o', 'output.hfst']
           + symbolharm
           + flagharm
           + ['input1.hfst', 'input2.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'output.hfst',
            version = 'hfst-concatenate' if VersionLog == 'produce' else None)
