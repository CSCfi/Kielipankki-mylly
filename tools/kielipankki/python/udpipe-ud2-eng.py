# TOOL udpipe-ud2-eng.py: "Parse text with UD2-English model" (Segment and parse English plaintext according to the Universal Dependencies version 2.)
# INPUT input.txt TYPE GENERIC
# OUTPUT ud2.txt
# OUTPUT ud2.tsv
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
from lib_udpipe import parse_plain

name('ud2.txt', '{}-ud2'.format(base('input.txt', '*.txt')),
     ins = 'en', ext = 'txt')
name('ud2.tsv', '{}-ud2'.format(base('input.txt', '*.txt')),
     ins = 'en', ext = 'rel.tsv')

# makes ud2.txt.tmp, ud2.tsv.tmp, or exits with error message in stderr
parse_plain('english-ud-2.0-170801.udpipe',
            'input.txt',
            'ud2.txt.tmp', 'ud2.tsv.tmp')

os.rename('ud2.txt.tmp', 'ud2.txt')
os.rename('ud2.tsv.tmp', 'ud2.tsv')
