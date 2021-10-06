# TOOL hfst-fst2fst.py: "Convert archive format"
# (Converts a HFST transducer archive to another format. Default is OpenFST format with tropical weights.)
# INPUT input.hfst: "Transducers" TYPE GENERIC
#     (An HFST transducer archive)
# OUTPUT output.hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Format
#     TYPE [tropical: "OpenFST Tropical",
#           logarithmic: "OpenFST Log",
#           weighted: "Optimized lookup, weighted",
#           unweighted: "Optimized lookup, unweighted"]
#     DEFAULT tropical
#     (HFST binary format)
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

name('output.hfst', base('input.hfst', '*.hfst'),
     ins = 'convert',
     ext = 'hfst')

hfst.setenv(Version)

FMT = dict(tropical = 'openfst-tropical',
           logarithmic = 'openfst-log',
           weighted = 'optimized-lookup-weighted',
           unweighted = 'optimized-lookup-unweighted')[Format]

with Popen(['hfst-fst2fst', '-o', 'output.hfst',
            '--format', FMT,
            'input.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'output.hfst',
            version = 'hfst-fst2fst' if VersionLog == 'produce' else None)
