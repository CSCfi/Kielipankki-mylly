# TOOL hfst-summarize.py: "Report on a transducer" (Provides a summary report of the properties of a HFST transducer)
# INPUT ducer.hfst
# OUTPUT summary.txt
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER Version TYPE [v3121: "3.12.1", v3110: "3.11.0", v3090: "3.9.0", v3083: "3.8.3"] DEFAULT v3121 (HFST Version)
# RUNTIME python3

# (TODO) rename summary file according to the input file

them = dict(v3083 = '/homeappl/appl_taito/ling/hfst/3.8.3/bin/hfst-summarize',
            v3090 = '/homeappl/appl_taito/ling/hfst/3.9.0/bin/hfst-summarize',
            v3110 = '/homeappl/appl_taito/ling/hfst/3.11.0/bin/hfst-summarize',
            v3121 = '/homeappl/appl_taito/ling/hfst/3.12.1/bin/hfst-summarize')

import os
from subprocess import Popen
# Like, --help says -o names a transducer but it seems to name the
# report; hfst-summarize does not output a transducer. (Should be
# reported. TODO.)
with Popen([them[Version], '-o', 'summary.txt', 'ducer.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')):
    pass

# (TODO) remove empty stdout or stderr log
