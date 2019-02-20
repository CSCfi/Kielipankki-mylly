# TOOL vrt-finer.py: "Nertag Finnish VRT with FiNER" (Recognize and classify names and such in Finnish VRT.)
# INPUT input.vrt TYPE GENERIC
# OUTPUT output.vrt
# RUNTIME python3

import os, sys
from subprocess import Popen

# VRT tools are not yet installed in a proper place
# so Mylly has some temporary copies
PROG = os.path.join(chipster_module_path, 'python', 'xvrt-tools',
                    'vrt-finer')

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.vrt', base('input.vrt', '*.vrt.txt'),
     ext = 'vrt.txt')

fine = Popen(['python3', PROG],
             stdin = open('input.vrt', mode = 'rb'),
             stdout = open('output.tmp', mode = 'wb'))

status = fine.wait()
status and exit(status)

# with LC_ALL=C.UTF.8, vrt-fine finally finished succesfully
os.rename('output.tmp', 'output.vrt')
