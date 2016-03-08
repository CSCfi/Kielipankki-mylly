# TOOL test-multifile.py: "Multifile Test" (Receives and produces a pattern of files)
# INPUT input{...}.txt TYPE GENERIC (Input files, presumably)
# OUTPUT info.txt  (File attempts to reveal parameters and input files)
# OUTPUT output{...}.txt TYPE GENERIC (Odd-numbered output files)
# OUTPUT OPTIONAL error.txt  (Diagnostics if any)
# PARAMETER code TYPE [utf8: "UTF-8", latin1: "ISO-8859-1"] DEFAULT utf8

# Want to run this in Chipster and see
# - how one gets to set multiple input files in the user interface
# - how the script gets too see them
# - how output files appear back in user interface (maybe they do)

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
