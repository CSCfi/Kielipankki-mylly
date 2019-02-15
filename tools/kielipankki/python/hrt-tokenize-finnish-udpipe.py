# TOOL hrt-tokenize-finnish-udpipe.py: "Tokenize Finnish HRT with UDPipe" (Tokenize Finnish HRT into VRT with UDPipe.)
# INPUT input.hrt TYPE GENERIC
# OUTPUT output.vrt
# OUTPUT error.log
# OUTPUT OPTIONAL ls-out.log
# OUTPUT OPTIONAL ls-err.log
# RUNTIME python3

import os, sys
from subprocess import Popen

# VRT tools are not yet installed in a proper place
# so Mylly has some temporary copies
PROG = os.path.join(chipster_module_path, 'python', 'xvrt-tools',
                    'hrt-tokenize-udpipe')

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.vrt', base('input.hrt', '*.hrt.txt'),
     ext = 'vrt.txt')

try:
    with Popen(['python3', PROG],
               stdin = open('input.hrt', mode = 'rb'),
               stdout = open('output.vrt', mode = 'wb'),
               stderr = open('error.log', mode = 'wb')) as tokenize:
        pass
except Exception as exn:
    et, ev, tr = sys.exc_info()
    print(et, ev, tr, sep = '\n', file = sys.stderr)

# still trying to see why PROG is not found
with Popen(['ls', '-ldF',
            '/appl',
            '/appl/ling',
            '/appl/ling/udpipe'],
           stdout = open('ls-out.log', mode = 'wb'),
           stderr = open('ls-err.log', mode = 'wb')) as whatever:
    pass
# exit(1)
