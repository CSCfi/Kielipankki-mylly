# TOOL vrt-finer.py: "Nertag Finnish VRT with FiNER" (Recognize and classify names and such in Finnish VRT.)
# INPUT input.vrt TYPE GENERIC
# OUTPUT output.vrt
# OUTPUT error.log
# RUNTIME python3

import os, sys
from subprocess import Popen, TimeoutExpired

# VRT tools are not yet installed in a proper place
# so Mylly has some temporary copies
PROG = os.path.join(chipster_module_path, 'python', 'xvrt-tools',
                    'vrt-finer')

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.vrt', base('input.vrt', '*.vrt.txt'),
     ext = 'vrt.txt')

try:
    fine = Popen(['python3', PROG],
                 stdin = open('input.vrt', mode = 'rb'),
                 stdout = open('output.tmp', mode = 'wb')
                 # stderr = open('error.log', mode = 'wb')
    )
    status = fine.wait(20)

except TimeoutExpired as exn:
    # just so there is output.vrt so chipster let one see error.log,
    # hopefully to find out why the job stalls over there
    os.rename('output.tmp', 'output.vrt')

except Exception as exn:
    et, ev, tr = sys.exc_info()
    print(et, ev, tr, sep = '\n', file = sys.stderr)
    exit(2)

os.rename('output.tmp', 'output.vrt')
