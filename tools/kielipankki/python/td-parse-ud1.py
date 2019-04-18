# TOOL td-parse-ud1.py: "Parse Finnish plaintext /TDP UD1" (Segments Finnish plaintext into sentences and tokens. Annotates each sentence with a morpho-syntactic structure using an UD1 version of the Turku Dependency Parser.)
# INPUT input.txt TYPE GENERIC
# OUTPUT output.txt
# RUNTIME python3

import os, sys
from subprocess import Popen

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.txt', '{}-ud1'.format(base('input.txt', '*.txt')),
     ext = 'txt')

# see if default finnish-parse works in Mylly 2019-04-18

with Popen([ '/appl/ling/finnish-parse/1.0/bin/finnish-parse' ],
           stdin  = open('input.txt', mode = 'rb'),
           stdout = open('output.txt', mode = 'wb')) as parse:
    pass
