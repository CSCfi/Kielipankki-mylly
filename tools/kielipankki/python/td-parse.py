# TOOL td-parse.py: "Parse Finnish plaintext /TDP Old" (Segments Finnish plaintext into sentences and tokens. Annotates each sentence with a morpho-syntactic structure using an early version of the Turku Dependency Parser.)
# INPUT input.txt TYPE GENERIC
# OUTPUT output.txt
# IMAGE comp-16.04-mylly
# RUNTIME python3

import os, sys
from subprocess import Popen

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.txt', '{}-dep'.format(base('input.txt', '*.txt')),
     ext = 'txt')

# ok, it does produce output stdin->stdout in Taito, eventually, so
# try in Mylly - there would be 7 output fields in case one wants to
# process the output somehow, but does it work without environment?
# be seen - yeah, right, it tells in *stdout* that "Parser not found
# in
# /appl//ling/finnish-parse/1.0/share/Finnish-dep-parser/alpha-custom"

print('ls -R /appl//ling/finnish-parse/, hopefully,',
      'and no idea why such double slashes',
      sep = '\n')

with Popen([ 'ls', '-R',
             '/appl//ling/finnish-parse/' ]) as sigh:
    pass

with Popen([ '/appl/ling/finnish-parse/1.0/bin/finnish-parse',
             '--stanford' ],
           # env = dict(os.environ, TMPDIR = os.getcwd()),
           stdin  = open('input.txt', mode = 'rb'),
           stdout = open('output.txt', mode = 'wb')) as parse:
    pass
