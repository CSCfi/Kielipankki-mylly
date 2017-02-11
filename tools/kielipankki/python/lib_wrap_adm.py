# This script is imported in the wrap-adm.py tool if the user knows
# something. Otherwise this script is inaccessible, so the user will
# not even know what mildly sensitive issues it would have revealed.
# (Those with access to the private repository are, of course,
# trusted.)

# The immediate intent is to gather information that is relevant to
# the development of the use of the batch system through mylly.

import glob
import os
import shutil
from subprocess import Popen, PIPE
from zipfile import ZipFile

def dispatch(out, action, ticket):
    print('action == {!r}'.format(action),
          'ticket == {!r}'.format(ticket),
          '',
          sep = '\n',
          file = out)

    if action == 'info':
        print_info(out)
    elif action == 'remove':
        remove_wrap_directory(out, ticket)
    else:
        print('Unrecognized action? This cannot happen!',
              file = out)

def print_info(out):
    print('Node: {}'.format(os.uname().nodename),
          'USER={}'.format(os.environ.get('USER')),
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

def remove_wrap_directory(out, ticket):
    '''Remove $WRKDIR/ticket, if there and so on. An ordinary user of
    Mylly must never get access to this operation except through their
    own job file, and they must never get access to a job file of
    someone else. This is delicate.
    '''
    wrapwork = os.path.join(os.environ.get('WRKDIR'), ticket)
    print('Removing {!r}'.format(wrapwork),
          file = out)

    if os.path.isdir(wrapwork):
        print('There is such directory', file = out)
    else:
        print('Failing: there is no such directory', file = out)
        return

    if ticket.startswith('wrap'):
        print('Ticket starts with "wrap"', file = out)
    else:
        print('Failing: ticket does not start with "wrap"', file = out)
        return

    # TODO: if the wrap directory records the job as started and the
    # job is still in the batch system, warn without removing.

    # TODO: if the wrap directory records the job as started but the
    # job is not in the batch system - what then?

    print("Actually removing the directory", file = out)
    shutil.rmtree(wrapwork)
