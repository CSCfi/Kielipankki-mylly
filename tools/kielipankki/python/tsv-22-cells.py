# TOOL tsv-22-cells.py: "Contingency tables as cells"
# (Make contingency tables for two combinations of relation attributes. Joint count is named cM12, other counts cM1o, cMo2, cMoo. The component attribute names are suffixed with of1 and of2.)
# INPUT datum.tsv TYPE GENERIC
# OUTPUT table.tsv
# PARAMETER one0 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER one1 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER one2 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER one3 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER two0 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER two1 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER two2 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER two3 TYPE COLUMN_SEL DEFAULT "EMPTY"
# RUNTIME python3

from collections import Counter
from itertools import chain
import os

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('table.tsv', '{}-22cel'.format(base('datum.tsv', '*.rel.tsv')),
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

one = sorted(set(name for name in (one0, one1, one2, one3)
                 if name not in ("EMPTY", "")))

two = sorted(set(name for name in (two0, two1, two2, two3)
                 if name not in ("EMPTY", "")))

with open('datum.tsv') as data:
    head = next(data).rstrip('\n').split('\t')
    take1 = index(head, one)
    take2 = index(head, two)
    them = Counter((value(record, take1), value(record, take2))
                   for line in data
                   for record in [line.rstrip('\n').split('\t')])

ones = Counter(r for r, k in them.elements())
twos = Counter(k for r, k in them.elements())

total = sum(them.values())

with open('table.tmp', mode = 'w', encoding = 'utf-8') as out:
    print(*chain(('cM12', 'cM1o', 'cMo2', 'cMoo'),
                 map('{}of1'.format, value(head, take1)),
                 map('{}of2'.format, value(head, take2))),
          sep = '\t', file = out)
    for rk, c in them.items():
        r, k = rk
        print(c, ones[r] - c, twos[k] - c,
              total - c - (ones[r] - c) - (twos[k] - c),
              *chain(r, k),
              sep = '\t', file = out)

os.rename('table.tmp', 'table.tsv')
