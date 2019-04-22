# TOOL hrt-tokenize-finnish-hfst.py: "Tokenize Finnish HRT /HFST" (Tokenize Finnish HRT into VRT with HFST.)
# INPUT input.hrt TYPE GENERIC
# OUTPUT output.vrt
# RUNTIME python3

import os, sys
from subprocess import Popen

# VRT tools are not yet installed in a proper place
# so Mylly has some temporary copies
PROG = os.path.join(chipster_module_path, 'python', 'xvrt-tools',
                    'hrt-tokenize-finnish-hfst')

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.vrt', base('input.hrt', '*.hrt.txt'),
     ext = 'vrt.txt')

proc = Popen(['python3', PROG],
             stdin = open('input.hrt', mode = 'rb'),
             stdout = open('output.tmp', mode = 'wb'))

status = proc.wait()
status and exit(status)

os.rename('output.tmp', 'output.vrt')
