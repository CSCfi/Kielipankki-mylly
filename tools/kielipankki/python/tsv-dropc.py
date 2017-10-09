# TOOL tsv-dropc.py: "Drop/count selected attributes"
# (Drop selected attributes. Add counts. Prefix cM of count name indicates numeric type for some tools. EMPTY is not a name.)
# INPUT wide.tsv TYPE GENERIC
# OUTPUT narrow.tsv
# PARAMETER count TYPE COLUMN_SEL DEFAULT "cMcount"
# PARAMETER OPTIONAL drop0 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL drop1 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL drop2 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL drop3 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL drop4 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL drop5 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL drop6 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL drop7 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL drop8 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL drop9 TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL dropA TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL dropB TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL dropC TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL dropD TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL dropE TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL dropF TYPE COLUMN_SEL DEFAULT "EMPTY"
# RUNTIME python3

from collections import Counter
import os

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.enforce('wide.tsv', '.tsv')
names.output('narrow.tsv', names.replace('wide.tsv', '-drop.tsv'))

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

drop = set(name for name in (drop0, drop1, drop2, drop3,
                             drop4, drop5, drop6, drop7,
                             drop8, drop9, dropA, dropB,
                             dropC, dropD, dropE, dropF)
           if name not in ("EMPTY", ""))

with open('wide.tsv') as wide:
    head = next(wide).rstrip('\n').split('\t')
    take = index(head, set(head) - drop)
    them = Counter(value(line.rstrip('\n').split('\t'), take)
                   for line in wide)

if count in value(head, take):
    print('count name {} is one of the kept names:'.format(repr(count)),
          file = sys.stderr)
    print(*value(head, take), file = sys.stderr)
    exit(1)

with open('narrow.tmp', mode = 'w', encoding = 'utf-8') as out:
    print(count, *value(head, take), sep = '\t', file = out)
    for it in them:
        print(them[it], *it, sep = '\t', file = out)

os.rename('narrow.tmp', 'narrow.tsv')
