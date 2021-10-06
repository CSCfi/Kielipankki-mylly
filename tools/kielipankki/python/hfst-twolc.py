# TOOL hfst-twolc.py: "Compile a two-level grammar"
#     (Compiles a two-level grammar into an archive of rule transducers.)
# INPUT grammar.txt: "Grammar" TYPE GENERIC
#     (A two-level rule file)
# OUTPUT ducer.hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Format
#     TYPE [tropical: "OpenFST Tropical",
#           logarithmic: "OpenFST Log"]
#     DEFAULT tropical
#     (HFST binary format)
# PARAMETER ResolveLeft
#     TYPE [yes: "yes",
#           no: "no"]
#     DEFAULT no
#     (Whether to resolve left-arrow conflicts)
# PARAMETER ResolveRight
#     TYPE [yes: "yes",
#           no: "no"]
#     DEFAULT yes
#     (Whether to resolve right-arrow conflict)
# PARAMETER Version TYPE [v_3_14_0: "3.14.0"] DEFAULT v_3_14_0 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# IMAGE comp-16.04-mylly
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
import lib_hfst as hfst

import glob, os, shutil
from subprocess import Popen

name('ducer.hfst', base('grammar.txt', '*.txt'),
     ext = 'hfst')

hfst.setenv(Version)

FMT = dict(tropical = 'openfst-tropical',
           logarithmic = 'openfst-log')[Format]

resolveleft = dict(yes = ['--resolve'],
                   no = [])[ResolveLeft]

resolveright = dict(yes = [],
                    no = ['--dont-resolve-right'])[ResolveRight]

with Popen(['hfst-lexc', '-o', 'ducer.hfst',
            '--format', FMT]
           + resolveleft
           + resolveright
           ['grammar.txt'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'ducer.hfst',
            version = 'hfst-twolc' if VersionLog == 'produce' else None)
