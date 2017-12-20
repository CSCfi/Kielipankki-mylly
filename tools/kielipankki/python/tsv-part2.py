# TOOL tsv-part2.py: "Part and complement by value of attribute"
# (Makes a part of a relation containing those records that have the given value for the given attribute, and a part containing the other records.)
# INPUT one.tsv TYPE GENERIC
# OUTPUT part.tsv
# OUTPUT rest.tsv
# PARAMETER attr: "attribute name" TYPE COLUMN_SEL
# PARAMETER val: "attribute value" TYPE STRING
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('part.tsv', '{}-part'.format(base('one.tsv', '*.rel.tsv')),
     ext = 'rel.tsv')
name('rest.tsv', '{}-rest'.format(base('one.tsv', '*.rel.tsv')),
     ext = 'rel.tsv')

if attr in ("EMPTY", ""):
    print("need valid attribute", file = sys.stderr)
    exit(1)

with open('one.tsv', encoding = 'utf-8') as fin:
    with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
        with open('others.tmp', mode = 'w', encoding = 'utf-8') as oth:
            head = next(fin).rstrip('\n').split('\t')
            print(*head, sep = '\t', file = out)
            print(*head, sep = '\t', file = oth)
            ix = head.index(attr)
            for record in (tuple(line.rstrip('\n').split('\t'))
                           for line in fin):
                print(*record, sep = '\t',
                      file = out if record[ix] == val else oth)

os.rename('result.tmp', 'part.tsv')
os.rename('others.tmp', 'rest.tsv')
