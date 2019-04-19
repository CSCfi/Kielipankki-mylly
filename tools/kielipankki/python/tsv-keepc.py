# TOOL tsv-keepc.py: "Keep/count selected attributes"
# (Keep selected attributes. Add counts. Prefix cM of count name indicates numeric type for some tools.)
# INPUT wide.tsv TYPE GENERIC
# OUTPUT narrow.tsv
# PARAMETER count TYPE STRING DEFAULT "cMcount"
# PARAMETER OPTIONAL keep0 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keep1 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keep2 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keep3 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keep4 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keep5 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keep6 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keep7 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keep8 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keep9 TYPE COLUMN_SEL
# PARAMETER OPTIONAL keepA TYPE COLUMN_SEL
# PARAMETER OPTIONAL keepB TYPE COLUMN_SEL
# PARAMETER OPTIONAL keepC TYPE COLUMN_SEL
# PARAMETER OPTIONAL keepD TYPE COLUMN_SEL
# PARAMETER OPTIONAL keepE TYPE COLUMN_SEL
# PARAMETER OPTIONAL keepF TYPE COLUMN_SEL
# RUNTIME python3

from collections import Counter
import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('narrow.tsv', base('wide.tsv', '*.rel.tsv'),
     ins = 'keepc',
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

keep = tuple(name for name in (keep0, keep1, keep2, keep3,
                               keep4, keep5, keep6, keep7,
                               keep8, keep9, keepA, keepB,
                               keepC, keepD, keepE, keepF)
             if name)

if len(set(keep)) < len(keep):
    print('multiple selection:', file = sys.stderr)
    print(*keep, sep = '\n', file = sys.stderr)
    exit(1)

if count in keep:
    print('count name {} is one of the kept names:'.format(repr(count)),
          file = sys.stderr)
    print(*keep, sep = '\n', file = sys.stderr)
    exit(1)

with open('wide.tsv', mode = 'r', encoding = 'UTF-8') as wide:
    head = next(wide).rstrip('\n').split('\t')
    take = index(head, keep)
    them = Counter(value(line.rstrip('\n').split('\t'), take)
                   for line in wide)

with open('narrow.tmp', mode = 'w', encoding = 'UTF-8') as out:
    print(count, *value(head, take), sep = '\t', file = out)
    for it in them:
        print(them[it], *it, sep = '\t', file = out)

os.rename('narrow.tmp', 'narrow.tsv')
