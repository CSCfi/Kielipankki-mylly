# TOOL tsv-22-columns.py: "Contingency tables as columns"
# (Make contingency tables for two combinations relation attributes. Joint count is named cM12, other count cM1o, and column sums cMs2 and cMso. The component attribute names are suffixed with of1 and of2.)
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
import lib_names as names

names.enforce('datum.tsv', '.tsv')
names.output('table.tsv', names.replace('datum.tsv', '-22col.tsv'))

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
    print(*chain(('cM12', 'cM1o', 'cMs2', 'cMso'),
                 map('{}of1'.format, value(head, take1)),
                 map('{}of2'.format, value(head, take2))),
          sep = '\t', file = out)
    for rk, c in them.items():
        r, k = rk
        print(c, ones[r] - c, twos[k], total - twos[k],
              *chain(r, k),
              sep = '\t', file = out)

os.rename('table.tmp', 'table.tsv')
