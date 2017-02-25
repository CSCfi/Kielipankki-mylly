# TOOL hfst-summarize.py: "Report on a transducer" (Provides a summary report of the properties of a HFST transducer)
# INPUT ducer.hfst TYPE GENERIC
# OUTPUT summary.txt
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Version TYPE [v_3_12_1: "3.12.1", v_3_11_0: "3.11.0", v_3_9_0: "3.9.0", v_3_8_3: "3.8.3"] DEFAULT v_3_12_1 (HFST version)
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names # (TODO) rename summary file according to the input file
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

hfst.setenv(Version)

# Like, --help says -o names a transducer but it seems to name the
# report; hfst-summarize does not output a transducer. (Should be
# reported. TODO.)
with Popen(['hfst-summarize', '-o', 'summary.txt', 'ducer.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

# to see the optional results when the required result fails to be
if not os.path.exists('summary.txt'):
    with open('summary.txt', 'a'):
        pass

# sigh -
with Popen(['hfst-summarize', '--version'],
           stdout = open('stdout.log', 'ab'),
           stderr = open('stderr.log', 'ab')) as it:
    pass

# (TODO) remove empty stdout or stderr log
