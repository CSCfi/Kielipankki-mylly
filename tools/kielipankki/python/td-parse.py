# TOOL td-parse.py: "Parse Finnish plaintext /TDP (alpha)" (Segments Finnish plaintext into sentences and tokens. Annotates each sentence with a morpho-syntactic structure using an early version of the Turku Dependency Parser.)
# INPUT input.txt TYPE GENERIC
# OUTPUT output.txt
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.txt', '{}-dep'.format(base('input.txt', '*.txt')),
     ext = 'txt')

# ok, it does produce output stdin->stdout in Taito, eventually, so
# try in Mylly - there would be 7 output fields in case one wants to
# process the output somehow, but does it work without environment?
# be seen

with Popen([ '/appl/ling/finnish-parse/1.0/bin/finnish-parse',
             '--stanford' ],
           # env = dict(os.environ, TMPDIR = os.getcwd()),
           stdin  = open('input.txt', mode = 'rb'),
           stdout = open('output.txt', mode = 'wb')) as parse:
    pass
