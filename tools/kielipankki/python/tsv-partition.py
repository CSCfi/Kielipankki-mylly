# TOOL tsv-partition.py: "Partition a relation by a given attribute"
# (Makes a partition of a relation into parts with a particular value for the given attribute.)
# INPUT one.tsv: "Relation" TYPE GENERIC
#     (A relational TSV file)
# OUTPUT part{...}.tsv
# PARAMETER attr: "attribute name" TYPE COLUMN_SEL
# PARAMETER many: "maximum number of parts" TYPE INTEGER FROM 2 TO 30 DEFAULT 6
# IMAGE comp-16.04-mylly
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

# broken? when output files are part1.tsv, ... TODO
name('part.tsv', base('one.tsv', '*.tsv') + 'part',
     ext = 'tsv')

if attr in ("EMPTY", ""):
    print("need valid attribute", file = sys.stderr)
    exit(1)

with open('one.tsv', encoding = 'utf-8') as fin:
    head = next(fin).rstrip('\n').split('\t')
    data = list(tuple(line.rstrip('\n').split('\t')) for line in fin)

ix = head.index(attr)
vals = set(record[ix] for record in data)

if len(vals) > many:
    print('too many parts:', file = sys.stderr)
    print('attribute {} has {} different values'
          .format(repr(attr), len(vals)),
          file = sys.stderr)
    print('maximum number of parts is set to {}'
          .format(many),
          file = sys.stderr)
    exit(1)

outs = { val : open('part{}.tmp'.format(k), mode = 'w', encoding = 'utf-8')
         for k, val in enumerate(vals) }

for out in outs.values():
    print(*head, sep = '\t', file = out)

for record in data:
    print(*record, sep = '\t', file = outs[record[ix]])

for out in outs.values():
    out.close()

for k, val in enumerate(outs):
    os.rename('part{}.tmp'.format(k),
              'part{}.tsv'.format(k))
