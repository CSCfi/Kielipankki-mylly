# TOOL tsv-part.py: "Part with value of an attribute"
# (Makes a part of a relation containing those records that have the given value for the given attribute.)
# INPUT one.tsv TYPE GENERIC
# OUTPUT part.tsv
# PARAMETER attr: "attribute name" TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER val: "attribute value" TYPE STRING
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('part.tsv', base('one.tsv', '*.rel.tsv'),
     ins = 'part',
     ext = 'rel.tsv')

if attr in ("EMPTY", ""):
    print("need valid attribute", file = sys.stderr)
    exit(1)

with open('one.tsv', encoding = 'utf-8') as fin:
    with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
        head = next(fin).rstrip('\n').split('\t')
        print(*head, sep = '\t', file = out)
        ix = head.index(attr)
        for record in (tuple(line.rstrip('\n').split('\t'))
                       for line in fin):
            if record[ix] == val:
                print(*record, sep = '\t', file = out)

os.rename('result.tmp', 'part.tsv')
