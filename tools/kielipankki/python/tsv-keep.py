# TOOL tsv-keep.py: "Keep selected attributes"
# (Keep only the selected attributes. EMPTY is not a name.)
# INPUT wide.tsv: "input relation" TYPE GENERIC
# OUTPUT narrow.tsv
# PARAMETER OPTIONAL keep0 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keep1 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keep2 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keep3 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keep4 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keep5 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keep6 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keep7 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keep8 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keep9 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keepA TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keepB TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keepC TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keepD TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keepE TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL keepF TYPE COLUMN_SEL DEFAULT "EMPTY"
# RUNTIME python3

from collections import Counter
import os

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('narrow.tsv', base('wide.tsv', '*.rel.tsv'),
     ins = 'keep',
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

keep = set(name for name in (keep0, keep1, keep2, keep3,
                             keep4, keep5, keep6, keep7,
                             keep8, keep9, keepA, keepB,
                             keepC, keepD, keepE, keepF)
           if name not in ("EMPTY", ""))

with open('wide.tsv') as wide:
    head = next(wide).rstrip('\n').split('\t')
    take = index(head, keep)
    them = Counter(value(line.rstrip('\n').split('\t'), take)
                   for line in wide)

with open('narrow.tmp', mode = 'w', encoding = 'utf-8') as out:
    print(*value(head, take), sep = '\t', file = out)
    for it in them:
        print(*it, sep = '\t', file = out)

os.rename('narrow.tmp', 'narrow.tsv')
