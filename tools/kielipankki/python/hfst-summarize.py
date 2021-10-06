# TOOL hfst-summarize.py: "Describe an archive"
# (Produces a summary description for an HFST transducer archive)
# INPUT ducer.hfst: "Transducers" TYPE GENERIC
#     (An HFST transducer archive)
# OUTPUT summary.txt
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
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

name('summary.txt', base('ducer.hfst', '*.hfst'),
     ins = 'summary',
     ext = 'txt')

hfst.setenv(Version)

# hfst-summarize --help says -o names a transducer but it seems to
# name the summary report, and hfst-summarize does not output a
# transducer. (Should be reported. Is it still the case? TODO.)

with Popen(['hfst-summarize', '-o', 'summary.txt', 'ducer.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'summary.txt',
            version = 'hfst-summarize' if VersionLog == 'produce' else None)
