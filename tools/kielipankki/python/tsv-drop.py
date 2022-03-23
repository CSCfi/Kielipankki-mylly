# TOOL tsv-drop.py: "Drop selected attributes"
# (Drop the selected attributes.)
# INPUT wide.tsv TYPE GENERIC
# OUTPUT narrow.tsv
# PARAMETER OPTIONAL drop0 TYPE COLUMN_SEL
# PARAMETER OPTIONAL drop1 TYPE COLUMN_SEL
# PARAMETER OPTIONAL drop2 TYPE COLUMN_SEL
# PARAMETER OPTIONAL drop3 TYPE COLUMN_SEL
# PARAMETER OPTIONAL drop4 TYPE COLUMN_SEL
# PARAMETER OPTIONAL drop5 TYPE COLUMN_SEL
# PARAMETER OPTIONAL drop6 TYPE COLUMN_SEL
# PARAMETER OPTIONAL drop7 TYPE COLUMN_SEL
# PARAMETER OPTIONAL drop8 TYPE COLUMN_SEL
# PARAMETER OPTIONAL drop9 TYPE COLUMN_SEL
# PARAMETER OPTIONAL dropA TYPE COLUMN_SEL
# PARAMETER OPTIONAL dropB TYPE COLUMN_SEL
# PARAMETER OPTIONAL dropC TYPE COLUMN_SEL
# PARAMETER OPTIONAL dropD TYPE COLUMN_SEL
# PARAMETER OPTIONAL dropE TYPE COLUMN_SEL
# PARAMETER OPTIONAL dropF TYPE COLUMN_SEL

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
           if name)

with open('wide.tsv', mode = 'r', encoding = 'UTF-8') as wide:
    head = next(wide).rstrip('\n').split('\t')
    take = index(head, tuple(name for name in head
                             if name not in drop))
    them = Counter(value(line.rstrip('\n').split('\t'), take)
                   for line in wide)

with open('narrow.tmp', mode = 'w', encoding = 'UTF-8') as out:
    print(*value(head, take), sep = '\t', file = out)
    for it in them:
        print(*it, sep = '\t', file = out)

os.rename('narrow.tmp', 'narrow.tsv')
