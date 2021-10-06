# TOOL tsv-drop-sans.py: "Drop selected attributes without COLUMN_SEL"
# (Drop the selected attributes. EMPTY is not a name.)
# INPUT wide.tsv TYPE GENERIC
# OUTPUT narrow.tsv
# PARAMETER OPTIONAL drop0 TYPE STRING
# PARAMETER OPTIONAL drop1 TYPE STRING
# PARAMETER OPTIONAL drop2 TYPE STRING
# PARAMETER OPTIONAL drop3 TYPE STRING
# PARAMETER OPTIONAL drop4 TYPE STRING
# PARAMETER OPTIONAL drop5 TYPE STRING
# PARAMETER OPTIONAL drop6 TYPE STRING
# PARAMETER OPTIONAL drop7 TYPE STRING
# PARAMETER OPTIONAL drop8 TYPE STRING
# PARAMETER OPTIONAL drop9 TYPE STRING
# PARAMETER OPTIONAL dropA TYPE STRING
# PARAMETER OPTIONAL dropB TYPE STRING
# PARAMETER OPTIONAL dropC TYPE STRING
# PARAMETER OPTIONAL dropD TYPE STRING
# PARAMETER OPTIONAL dropE TYPE STRING
# PARAMETER OPTIONAL dropF TYPE STRING
# IMAGE comp-16.04-mylly
# RUNTIME python3

from collections import Counter
import os

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('narrow.tsv', base('wide.tsv', '*.rel.tsv'),
     ins = 'drop',
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

drop = set(name for name in (drop0, drop1, drop2, drop3,
                             drop4, drop5, drop6, drop7,
                             drop8, drop9, dropA, dropB,
                             dropC, dropD, dropE, dropF)
           if name not in ("EMPTY", ""))

with open('wide.tsv', encoding = 'UTF-8') as wide:
    head = next(wide).rstrip('\n').split('\t')
    take = index(head, set(head) - drop)
    them = Counter(value(line.rstrip('\n').split('\t'), take)
                   for line in wide)

with open('narrow.tmp', mode = 'w', encoding = 'UTF-8') as out:
    print(*value(head, take), sep = '\t', file = out)
    for it in them:
        print(*it, sep = '\t', file = out)

os.rename('narrow.tmp', 'narrow.tsv')
