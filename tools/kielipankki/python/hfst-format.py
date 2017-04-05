# TOOL hfst-format.py: "Determine archive format"
#     (Produces a brief report on which particular format the transducers in the archive are in.)
# INPUT ducer.hfst TYPE GENERIC
# OUTPUT format.txt
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Version TYPE [v_3_12_1: "3.12.1", v_3_11_0: "3.11.0", v_3_9_0: "3.9.0", v_3_8_3: "3.8.3"] DEFAULT v_3_12_1 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

names.output('format.txt', names.replace('ducer.hfst', '-format.txt'))
hfst.setenv(Version)

with Popen(['hfst-format', '-o', 'format.txt', 'ducer.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'summary.txt',
            version = 'hfst-summarize' if VersionLog == 'produce' else None)
