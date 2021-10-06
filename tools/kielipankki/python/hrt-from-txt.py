# TOOL hrt-from-txt.py: "Segment Finnish plaintext" (Segment Finnish plaintext into text and paragraph elements at empty lines. The output HRT format can then be tokenized into VRT.)
# INPUT input.txt TYPE GENERIC
# OUTPUT output.hrt
# IMAGE comp-16.04-mylly
# RUNTIME python3

import os, sys
from subprocess import Popen

# VRT tools are not yet installed in a proper place
# so Mylly has some temporary copies
PROG = os.path.join(chipster_module_path, 'python', 'xvrt-tools',
                    'hrt-from-txt')

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.hrt', base('input.txt', '*.txt'),
     ext = 'hrt.txt')

try:
    with Popen(['python3', PROG],
               stdin = open('input.txt', mode = 'rb'),
               stdout = open('output.hrt', mode = 'wb'),
               stderr = open('error.log', mode = 'wb')) as segment:
        pass
except Exception as exn:
    et, ev, tr = sys.exc_info()
    print(et, ev, tr, sep = '\n', file = sys.stderr)
    exit(1)
