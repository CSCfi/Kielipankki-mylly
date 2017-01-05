from glob import glob
import os

def consolidate():
    '''Append all non-empty error?*.log files to the one true error.log,
    headed by the file name, remove error?*.log, and finally remove
    even error.log if it is empty.

    This is meant to be used by tools that may produce more than one
    intermediate errorX.log but have promised to produce only one
    error.log as an optional output file.

    '''

    # Append in bytes. Because would not be smart to rely on erroneous
    # combinations of external tools for known reasonable encodings.

    log = b'error.log'

    if glob(log) and os.path.getsize(log) > 0:
        with open(log, mode = 'ab') as out:
            out.write(b'\n\n')

    for lox in sorted(glob(b'error?*.log')):
        if os.path.getsize(lox) > 0:
            with open(lox, mode = 'rb') as err, \
                 open(log, mode = 'ab') as out:
                out.write(b'=== ')
                out.write(lox)
                out.write(b':\n\n')
                out.write(err.read())
        os.remove(lox)

    if glob(log) and os.path.getsize(log) == 0:
        os.remove(log)
