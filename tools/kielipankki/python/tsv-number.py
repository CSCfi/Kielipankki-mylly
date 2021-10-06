# TOOL tsv-number.py: "Number records" (Number the records in such arbitrary order as they happen to be)
# INPUT data.tsv TYPE GENERIC
# OUTPUT result.tsv
# PARAMETER number: "Number field name" TYPE STRING DEFAULT "kMid"
# IMAGE comp-16.04-mylly
# RUNTIME python3

import os, sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('result.tsv', base('data.tsv', '*.rel.tsv'),
     ins = 'number',
     ext = 'rel.tsv')

try:
    with open('data.tsv', encoding = 'UTF-8') as data:
        head = next(data).rstrip('\n').split('\t')
        if number in head:
            raise ValueError('name is in use: {}'.format(number))
        with open('result.tsv', mode = 'w', encoding = 'UTF-8') as out:
            print(number, *head, sep = '\t', file = out)
            for k, line in enumerate(data, start = 1):
                print(k, line, sep = '\t', end = '', file = out)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)
