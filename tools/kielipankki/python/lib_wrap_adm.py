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

def dispatch(out, action, ticket):
    print('action == {!r}'.format(action),
          'ticket == {!r}'.format(ticket),
          '',
          sep = '\n',
          file = out)

    if action == 'info':
        print_info(out)
    elif action == 'delete':
        delete_wrap_directory(out, ticket)
    else:
        print('Unrecognized action? This cannot happen!',
              file = out)

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
        # These turned out to be redundant:
        # print(file = out)
        # print(wrap, end = ':\n', file = out)
        with Popen(['/bin/ls', '-R', '-lF', wrap],
                   stdout = PIPE,
                   stderr = PIPE) as p:
            o, e = p.communicate(timeout = 5)
            print(o.decode('UTF-8'),
                  file = out)

def delete_wrap_directory(out, ticket):
    wrapwork = os.path.join(os.environ.get('WRKDIR'), ticket)
    print('TODO: delete directory {!r}'
          .format(wrapwork),
          file = out)

    if os.path.isdir(wrapwork):
        print('which is there all right', file = out)
    else:
        print('which is not there! (or is not a directory)', file = out)

    if ticket.startswith('wrap'):
        print('ticket starts with "wrap" ok', file = out)
    else:
        print('ticket should start with "wrap"', file = out)
