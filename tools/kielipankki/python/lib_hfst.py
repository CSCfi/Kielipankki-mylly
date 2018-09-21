import os
from subprocess import Popen

def prepend_to_path(path, *entries):
    os.environ[path] = ( ':'.join((':'.join(entries),
                                   os.environ[path]))
                         .rstrip(':') )

def setenv(hfst_version):
    if hfst_version == 'v_3_14_0':
        prepend_to_path('PATH',
                        '/appl/ling/hfst/3.14.0/bin')
        prepend_to_path('LD_LIBRARY_PATH',
                        '/appl/ling/hfst/3.14.0/lib')
    else:
        # find out what is needed for summary v 3.14.0, then work on
        # other versions and other HFST programs
        raise ValueError('only implemented for 3.14.0')

def finish(require = None, version = None):
    '''Ensure that a required result file exists, by touching it if
    it otherwise doesn't. This is meant to satisfy chipster so that
    optional results can appear.

    If version command is given, use it to produce version.log, which
    can then be an optional output file.

    Also remove stdout.log and stderr.log if they exist but are
    empty. They can then be optional output files.'''

    if require is not None:
        require_result(require)

    if version is not None:
        log_version(version)

    for log in ('stdout.log', 'stderr.log'):
        if os.path.exists(log) and os.path.getsize(log) == 0:
            os.unlink(log)

def require_result(result):
    if not os.path.exists(result):
        with open(result, 'a'):
            pass

def log_version(command):
    with Popen([command, '--version'],
               stdout = open('version.log', 'ab'),
               stderr = open('stderr.log', 'ab')) as it:
        pass
