# TOOL hfst-twolc.py: "Compile a two-level grammar"
#     (Compiles a two-level grammar into an archive of rule transducers.)
# INPUT grammar.txt TYPE GENERIC
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
# PARAMETER Version TYPE [v_3_12_1: "3.12.1", v_3_11_0: "3.11.0", v_3_9_0: "3.9.0", v_3_8_3: "3.8.3"] DEFAULT v_3_12_1 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_hfst as hfst

import glob, os, shutil
from subprocess import Popen

# is it so that Chipster ensures there is at least grammar-1.txt?
names.output('ducer.hfst', names.replace('grammar.txt', '.hfst'))

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
