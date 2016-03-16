# TOOL test-parameters.py: "Parameterization Test" (Receives parameters)
# INPUT OPTIONAL hukairs.txt TYPE GENERIC (Whatever file, if any)
# OUTPUT info.txt  (File attempts to reveal parameters)
# OUTPUT OPTIONAL error.txt  (Diagnostics if any)
# PARAMETER code TYPE [utf8: "UTF-8", latin1: "ISO-8859-1"] DEFAULT utf8
# PARAMETER size TYPE INTEGER FROM 0 TO 1000 (Some number, nothing more.)
# PARAMETER OPTIONAL secret TYPE STRING (Something only you know!)

# Want to run this in Chipster and see
# - how one gets to set parameters in the user interface
# - how the script gets too see the parameters

import sys

with open('info.txt', 'wt') as f:
    print('sys.version:', sys.version, file = f)
    print(file = f)

    print('sys.argv:', file = f)
    for k, o in enumerate(sys.argv):
        print(k, o, sep = '\t', file = f)
    else:
        print(file = f)

    print('sys.path:', file = f)
    for k, o in enumerate(sys.path):
        print(k, o, sep = '\t', file = f)
    else:
        print(file = f)

    print('parameters:', file = f)
    print('code:', repr(code), sep = '\t', file = f)
    print('size:', repr(size), sep = '\t', file = f)
    print('secret:', repr(secret), sep = '\t', file = f)
