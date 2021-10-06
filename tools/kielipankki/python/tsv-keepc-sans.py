# TOOL tsv-keepc-sans.py: "Keep/count selected attributes without using COLUMN_SEL"
# (Keep selected attributes. Add counts. Prefix cM of count name indicates numeric type for some tools. EMPTY is not a name.)
# INPUT wide.tsv TYPE GENERIC
# OUTPUT narrow.tsv
# PARAMETER count TYPE STRING DEFAULT "cMcount"
# PARAMETER OPTIONAL keep0 TYPE STRING
# PARAMETER OPTIONAL keep1 TYPE STRING
# PARAMETER OPTIONAL keep2 TYPE STRING
# PARAMETER OPTIONAL keep3 TYPE STRING
# PARAMETER OPTIONAL keep4 TYPE STRING
# PARAMETER OPTIONAL keep5 TYPE STRING
# PARAMETER OPTIONAL keep6 TYPE STRING
# PARAMETER OPTIONAL keep7 TYPE STRING
# PARAMETER OPTIONAL keep8 TYPE STRING
# PARAMETER OPTIONAL keep9 TYPE STRING
# PARAMETER OPTIONAL keepA TYPE STRING
# PARAMETER OPTIONAL keepB TYPE STRING
# PARAMETER OPTIONAL keepC TYPE STRING
# PARAMETER OPTIONAL keepD TYPE STRING
# PARAMETER OPTIONAL keepE TYPE STRING
# PARAMETER OPTIONAL keepF TYPE STRING
# IMAGE comp-16.04-mylly
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

keep = set(name for name in (keep0, keep1, keep2, keep3,
                             keep4, keep5, keep6, keep7,
                             keep8, keep9, keepA, keepB,
                             keepC, keepD, keepE, keepF)
           if name not in ("EMPTY", ""))

if count in keep:
    print('count name {} is one of the kept names:'.format(repr(count)),
          file = sys.stderr)
    print(*keep, file = sys.stderr)
    exit(1)

with open('wide.tsv', encoding = 'UTF-8') as wide:
    head = next(wide).rstrip('\n').split('\t')
    take = index(head, keep)
    them = Counter(value(line.rstrip('\n').split('\t'), take)
                   for line in wide)

with open('narrow.tmp', mode = 'w', encoding = 'UTF-8') as out:
    print(count, *value(head, take), sep = '\t', file = out)
    for it in them:
        print(them[it], *it, sep = '\t', file = out)

os.rename('narrow.tmp', 'narrow.tsv')
