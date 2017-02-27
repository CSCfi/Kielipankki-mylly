# TOOL hfst-regexp2fst.py: "Compile regular expressions"
#     (Compiles regular expressions into transducers.)
# INPUT regexen.txt TYPE GENERIC
# OUTPUT duceren.hfst
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Format
#     TYPE [tropical: "OpenFST Tropical",
#           logarithmic: "OpenFST Log"]
#     DEFAULT tropical
#     (HFST binary format)
# PARAMETER Union
#     TYPE [many: "many transducers",
#           one: "one transducer"]
#     DEFAULT many
#     (How to represent the union of many regular expressions)
# PARAMETER Separator
#     TYPE [line: "line",
#           semicolon: "semicolon"]
#     DEFAULT line
#     (Separator between regular expressions)
# PARAMETER Version TYPE [v_3_12_1: "3.12.1", v_3_11_0: "3.11.0", v_3_9_0: "3.9.0", v_3_8_3: "3.8.3"] DEFAULT v_3_12_1 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

names.output('duceren.hfst', names.replace('regexen.txt', '.hfst'))

hfst.setenv(Version)

FMT = dict(tropical = 'openfst-tropical',
           logarithmic = 'openfst-log')[Format]

separator = dict(line = '--line',
                 semicolon = '--semicolon')[Separator]

unionmode = dict(many = [],
                 one = ['--disjunct'])[Union]

with Popen(['hfst-regexp2fst', '-o', 'duceren.hfst',
            '--format', FMT,
            separator]
           + unionmode
           + ['regexen.txt'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'duceren.hfst',
            version = 'hfst-regexp2fst' if VersionLog == 'produce' else None)
