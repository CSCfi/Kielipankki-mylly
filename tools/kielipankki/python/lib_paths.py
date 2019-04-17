import os, sys

def prepend(path, PATH):
    '''Sigh. And prepend a new path (a directory)
    to the value of an old PATH (an environment
    variable naming a sequence of directories).

    Return the new value. Do not set the environment!

    Except act surprised if the PATH was not even set.

    '''
    
    OLDPATH = os.getenv(PATH)
    if OLDPATH is None:
        print('environment variable', PATH, 'not set',
              file = sys.stderr)
        print('(this is unexpected - please report)',
              file = sys.stderr)
        exit(1)
    else:
        return os.pathsep.join((path, OLDPATH))
