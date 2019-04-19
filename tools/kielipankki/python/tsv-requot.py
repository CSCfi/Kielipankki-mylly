# TOOL tsv-requot.py: "Replace ASCII quotes" (Replace all ASCII quotes with right quotes.)
# INPUT data.tsv TYPE GENERIC
# OUTPUT result.tsv
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('result.tsv', base('data.tsv', '*.tsv'),
     ins = 'requot',
     ext = 'tsv')

reps = str.maketrans(( '\N{QUOTATION MARK}'
                       '\N{APOSTROPHE}' )
                     ,
                     ( '\N{RIGHT DOUBLE QUOTATION MARK}'
                       '\N{RIGHT SINGLE QUOTATION MARK}'
                     ))

try:
    with open('data.tsv', encoding = 'UTF-8') as data:
        head = next(data).rstrip('\n').split('\t')
        with open('result.tsv', mode = 'w', encoding = 'UTF-8') as out:
            print(*head, sep = '\t', file = out)
            for line in data:
                print(line.translate(reps),
                      sep = '\t',
                      end = '',
                      file = out)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)
