# This script is imported in the wrap-adm.py tool if the user knows
# something. Otherwise this script is inaccessible, so the user will
# not even know what mildly sensitive issues it would have revealed.
# (Those with access to the private repository are, of course,
# trusted.)

# The immediate intent is to gather information that is relevant to
# the development of the use of the batch system through mylly.

import glob
import os
from subprocess import Popen, PIPE

def print_info(out):
    print('USER={}'.format(os.environ.get('USER')),
          'WRKDIR={}'.format(os.environ.get('WRKDIR')),
          '',
          sep = '\n',
          file = out)
    with Popen(['/bin/ls', '-lF', os.environ.get('WRKDIR')],
               stdout = PIPE,
               stderr = PIPE) as p:
        o, e = p.communicate(timeout = 5)
        print(o.decode('UTF-8'),
              file = out)
    for wrap in sorted(glob.glob(os.path.join(os.environ.get('WRKDIR'), 'wrap*'))):
        print(file = out)
        print(wrap, end = ':\n', file = out)
        with Popen(['/bin/ls', '-R', '-lF', wrap],
                   stdout = PIPE,
                   stderr = PIPE) as p:
            o, e = p.communicate(timeout = 5)
            print(o.decode('UTF-8'),
                  file = out)
