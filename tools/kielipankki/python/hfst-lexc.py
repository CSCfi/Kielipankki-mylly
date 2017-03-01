# TOOL hfst-lexc.py: "Compile a lexical grammar"
#     (Compiles a lexical grammar into a transducer.)
# INPUT grammar{...}.txt TYPE GENERIC
# OUTPUT ducer.hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Format
#     TYPE [tropical: "OpenFST Tropical",
#           logarithmic: "OpenFST Log"]
#     DEFAULT tropical
#     (HFST binary format)
# PARAMETER AlignStrings
#     TYPE [yes: "yes",
#           no: "no"]
#     DEFAULT no
#     (Whether to align input and output strings)
# PARAMETER EncodeWeights
#     TYPE [yes: "yes",
#           no: "no"]
#     DEFAULT no
#     (Whether to encode weights when minimizing)
# PARAMETER WithFlags
#     TYPE [no: "no",
#           withflags: "use flags",
#           minimize: "use, and minimize their number",
#           rename: "use, minimize, and rename"]
#     DEFAULT no
#     (How to use flags to hyperminimize the result)
# PARAMETER FlagAs
#     TYPE [epsilon: "empty string",
#           symbol: "symbol"]
#     DEFAULT symbol
#     (How to treat a flag in composition, maybe)
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
names.output('ducer.hfst', names.replace('grammar-1.txt', '.hfst'))

hfst.setenv(Version)

FMT = dict(tropical = 'openfst-tropical',
           logarithmic = 'openfst-log')[Format]

align = dict(yes = ['--alignStrings'],
             no = [])[AlignStrings]

encode = dict(yes = ['--encode-weights'],
              no = [])[EncodeWeights]

withflags = dict(no = [],
                 withflags = ['--withFlags'],
                 minimize = ['--withFlags', '--minimizeFlags'],
                 rename = ['--withFlags',
                           '--minimizeFlags',
                           '--renameFlags'])[WithFlags]

flagas = dict(epsilon = ['--xerox-composition=no'],
              symbol = [])[FlagAs]

with Popen(['hfst-lexc', '-o', 'ducer.hfst',
            '--format', FMT]
           + align
           + encode
           + withflags
           + flagas
           + glob('grammar-*.txt'),
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'ducer.hfst',
            version = 'hfst-lexc' if VersionLog == 'produce' else None)
