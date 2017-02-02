# TOOL test-renaming.py: "Output File Rename Test" (Expose original names and eventually new names)
# INPUT first.txt TYPE GENERIC (First file)
# INPUT second.txt TYPE GENERIC (Second file)
# OUTPUT info.txt  (File attempts to reveal parameters)
# OUTPUT OPTIONAL chipster-inputs.tsv
# OUTPUT OPTIONAL chipster-outputs.tsv
# OUTPUT OPTIONAL error.txt  (Diagnostics if any)
# PARAMETER code TYPE [utf8: "UTF-8", latin1: "ISO-8859-1"] DEFAULT utf8
# PARAMETER size TYPE INTEGER FROM 0 TO 1000 (Some number, nothing more.)
# PARAMETER OPTIONAL secret TYPE STRING (Something only you know!)
# RUNTIME python3

# Initially just expose the otherwise hidden naming-mechanism files.
# To learn and to adapt. (This started as a copy of another tool.)

# Want to run this in Chipster and see
# - how one gets to set parameters in the user interface
# - how the script gets too see the parameters

import os, sys

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
    print(file = f)

    # Working out that the Python library location exists on the
    # server (in so far as it does - that is the question).

    print('/homeappl/home/kp-ruser/chipster/comp/modules:', file = f)
    for k, o in enumerate(sorted(os.listdir('/homeappl/home/kp-ruser/chipster/comp/modules'))):
        print(k, o, sep = '\t', file = f)
    else:
        print(file = f)
        
    common = '/homeappl/home/kp-ruser/chipster/comp/modules/common'
    if os.path.exists(common):
        if os.path.isdir(common):
            print(common, ':', sep = '\t', file = f)
            for k, o in enumerate(sorted(os.listdir(common))):
                print(k, o, sep = '\t', file = f)
            else:
                print(file = f)
        else:
            print(common, 'exists but is not a directory', file = f)
    else:
        print(common, 'does not exist', file = f)

    python3 = '/homeappl/home/kp-ruser/chipster/comp/modules/common/python3'
    if os.path.exists(python3):
        if os.path.isdir(python3):
            print(python3, ':', sep = '\t', file = f)
            for k, o in enumerate(sorted(os.listdir(python3))):
                print(k, o, sep = '\t', file = f)
            else:
                print(file = f)
        else:
            print(python3, 'exists but is not a directory', file = f)
    else:
        print(python3, 'does not exist', file = f)
