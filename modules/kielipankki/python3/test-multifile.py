# TOOL test-multifile.py: "Multifile Test" (Receives a pattern of files)
# INPUT input{...}.txt TYPE GENERIC (Input files, presumably)
# OUTPUT info.txt  (File attempts to reveal parameters and input files)
# OUTPUT OPTIONAL output.txt TYPE GENERIC (Guess cannot produce output in pattern)
# OUTPUT OPTIONAL error.txt  (Diagnostics if any)
# PARAMETER code TYPE [utf8: "UTF-8", latin1: "ISO-8859-1"] DEFAULT utf8

# Want to run this in Chipster and see
# - how one gets to set multiple input files in the user interface
# - how the script gets too see them
# - how output files appear back in user interface (maybe they do)
# An output-name pattern doesn't seem to work - at least got SADL error
# in chipster.log for output{...}.txt (unless it was alredy for the
# input{...}.txt, that is).

import os, sys

with open('info.txt', 'wt') as f:
    print('sys.version:', sys.version, file = f)
    print(file = f)

    print('sys.argv:', file = f)
    for k, o in enumerate(sys.argv):
        print(k, o, sep = '\t', file = f)
    else:
        print(file = f)

    print('os.getcwd():', file = f)
    print(os.getcwd(), end = '\n\n', file = f)

    print('os.listdir():', file = f)
    print(*os.listdir(), sep = '\n', file = f)
