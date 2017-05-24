# TOOL tsv-22-rows.py: "Contingency rows of two TSV combinations"
# (Contingency table of two combinations of TSV attributes as joint count cM12, other count cMo2, and row margins aka sums cM1s and cMos. The component attribute names are suffixed with of1 and of2.)
# INPUT datum.tsv TYPE GENERIC
# OUTPUT table.tsv
# PARAMETER          one0 TYPE STRING
# PARAMETER OPTIONAL one1 TYPE STRING
# PARAMETER OPTIONAL one2 TYPE STRING
# PARAMETER OPTIONAL one3 TYPE STRING
# PARAMETER          two0 TYPE STRING
# PARAMETER OPTIONAL two1 TYPE STRING
# PARAMETER OPTIONAL two2 TYPE STRING
# PARAMETER OPTIONAL two3 TYPE STRING
# RUNTIME python3

from collections import Counter
from itertools import chain
import os

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('table.tsv', names.replace('datum.tsv', '-22row.tsv'))

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

one = sorted(set(filter(None, (one0, one1, one2, one3))))
two = sorted(set(filter(None, (two0, two1, two2, two3))))

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
    print(*chain(('cM12', 'cM1s', 'cMo2', 'cMos'),
                 map('{}of1'.format, value(head, take1)),
                 map('{}of2'.format, value(head, take2))),
          sep = '\t', file = out)
    for rk, c in them.items():
        r, k = rk
        print(c, ones[r], twos[k], total - ones[r],
              *chain(r, k),
              sep = '\t', file = out)

os.rename('table.tmp', 'table.tsv')
