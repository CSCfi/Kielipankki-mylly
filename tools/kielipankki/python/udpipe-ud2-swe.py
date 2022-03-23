# TOOL udpipe-ud2-swe.py: "Parse Swedish plaintext /UDPipe LinES" (Segment and parse Swedish plaintext with UDPipe according to the Universal Dependencies version 2, LinES model.)
# INPUT input.txt TYPE GENERIC
# OUTPUT ud2.txt
# OUTPUT ud2.tsv

# https://github.com/UniversalDependencies/UD_Swedish-LinES

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
from lib_udpipe import parse_plain

name('ud2.txt', '{}-ud2'.format(base('input.txt', '*.txt')),
     ins = 'sv', ext = 'txt')
name('ud2.tsv', '{}-ud2'.format(base('input.txt', '*.txt')),
     ins = 'sv', ext = 'rel.tsv')

# makes ud2.txt.tmp, ud2.tsv.tmp, or exits with error message in stderr
parse_plain('swedish-lines',
            'input.txt',
            'ud2.txt.tmp', 'ud2.tsv.tmp')

os.rename('ud2.txt.tmp', 'ud2.txt')
os.rename('ud2.tsv.tmp', 'ud2.tsv')
