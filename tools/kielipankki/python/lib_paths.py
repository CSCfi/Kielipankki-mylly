import os, sys

def prepath(path):
    PATH = os.getenv('PATH')
    if PATH is None:
        print('PATH is not set',
              'This cannot happen',
              'Please report',
              sep = '\n',
              file = sys.stderr)
        exit(1)
    else:
        return os.pathsep.join((path, PATH))

def prelibs(path):
    return os.pathsep.join((path, os.getenv('LD_LIBRARY_PATH', '')))

def prepend(path, PATH):
    print('Deprecated function: lib_paths.prepend',
          'This should not be called any more',
          sep = '\n',
          file = sys.stderr)
    exit(1)
