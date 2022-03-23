# TOOL td-parse-ud1.py: "Parse Finnish plaintext /TDP UD1" (Segments Finnish plaintext into sentences and tokens. Annotates each sentence with a morpho-syntactic structure using an UD1 version of the Turku Dependency Parser.)
# INPUT input.txt TYPE GENERIC
# OUTPUT output.txt

import os, sys
from subprocess import Popen

sys.path.append(os.path.join(chipster_module_path, "python"))
sys.path.append(os.path.join(chipster_module_path, "python/xvrt-tools"))
from lib_names2 import base, name

from outsidelib import utf8ish

name('output.txt', '{}-ud1'.format(base('input.txt', '*.txt')),
     ext = 'txt')

# see if default finnish-parse works in Mylly 2019-04-18; it kind of
# seems to work but is full of question marks; see if a utf8ish locale
# helps - yes, it helps!

with Popen([ '/appl/ling/finnish-parse/1.0/bin/finnish-parse' ],
           env = dict(os.environ,
                      LC_ALL = utf8ish()),
           stdin  = open('input.txt', mode = 'rb'),
           stdout = open('output.txt', mode = 'wb')) as parse:
    pass
