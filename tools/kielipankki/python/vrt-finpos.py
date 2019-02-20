# TOOL vrt-finpos.py: "Postag Finnish VRT with FinnPos" (Classify words in Finnish VRT.)
# INPUT input.vrt TYPE GENERIC
# OUTPUT output.vrt
# RUNTIME python3

import os, sys
from subprocess import Popen

# VRT tools are not yet installed in a proper place
# so Mylly has some temporary copies
PROG = os.path.join(chipster_module_path, 'python', 'xvrt-tools',
                    'vrt-finpos')

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.vrt', base('input.vrt', '*.vrt.txt'),
     ins = 'pos',
     ext = 'vrt.txt')

postag = Popen(['python3', PROG, '--prefix=pos.'],
               stdin = open('input.vrt', mode = 'rb'),
               stdout = open('output.tmp', mode = 'wb'))

status = postag.wait()
status and exit(status)

os.rename('output.tmp', 'output.vrt')
