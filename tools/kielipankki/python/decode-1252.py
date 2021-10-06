# TOOL decode-1252.py: "Decode Windows-1252" (Convert Windows-1252 encoding to UTF-8)
# INPUT data.txt TYPE GENERIC
# OUTPUT text.txt
# IMAGE comp-16.04-mylly
# RUNTIME python3

import os, sys
from subprocess import Popen, DEVNULL

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import name, base

name('text.txt', base('data.txt', '*.txt'),
     ins = 'utf-8',
     ext = 'txt')

with Popen(['iconv', '-f', 'windows-1252', '-t', 'utf-8'],
           stdin = open('data.txt', 'rb'),
           stdout = open('text.tmp', 'wb'),
           stderr = DEVNULL) as iconv:
    pass # wait

if iconv.returncode is None:
    print('iconv did not finish', file = sys.stderr)
    iconv.kill()
    exit(1)

if iconv.returncode:
    print('iconv returned with {}'.format(iconv.returncode),
          file = sys.stderr)
    exit(1)

os.rename('text.tmp', 'text.txt')
