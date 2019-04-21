# TOOL hfst-summarize.py: "Describe an archive" (Produces a summary description about a HFST transducer archive)
# INPUT ducer.hfst TYPE GENERIC
# OUTPUT summary.txt
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Version TYPE [v_3_14_0: "3.14.0"] DEFAULT v_3_14_0 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name # TODO
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

names.output('summary.txt', names.replace('ducer.hfst', '-summary.txt'))
hfst.setenv(Version)

# hfst-summarize --help says -o names a transducer but it seems to
# name the summary report, and hfst-summarize does not output a
# transducer. (Should be reported. TODO.)

with Popen(['hfst-summarize', '-o', 'summary.txt', 'ducer.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'summary.txt',
            version = 'hfst-summarize' if VersionLog == 'produce' else None)
