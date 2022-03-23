# TOOL tsv-ext-prop.py: "Extend with proportions" (Extend relation with proportions over all records or over groups of records)
# INPUT input.tsv TYPE GENERIC
# OUTPUT output.tsv
# PARAMETER form TYPE [
#     flo: "float",
#     dec: "four decimals",
#     by3: "per thousand (round up)",
#     by6: "per million (round up)"
# ] DEFAULT flo
# PARAMETER prefix TYPE STRING DEFAULT wM
# PARAMETER count1 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER count2 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER count3 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER group1 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER group2 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER group3 TYPE COLUMN_SEL DEFAULT EMPTY

import os, re, sys
from itertools import chain, groupby
from operator import itemgetter
from math import ceil, fsum

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import name, base
from lib_sortedtsv import process

name('output.tsv', base('input.tsv', '*.rel.tsv'),
     ins = 'props',
     ext = 'rel.tsv')

countkeys = tuple(c for c in (count1, count2, count3)
                  if c not in ("EMPTY", ""))

groupkeys = tuple((g, 'default', 'increasing')
                  for g in (group1, group2, group3)
                  if g not in ("EMPTY", ""))

if not countkeys:
    print("no count attribute selected", file = sys.stderr)
    exit(1)

props = tuple(re.sub('^[a-z]+M|', prefix, attr, count = 1)
              for attr in countkeys)

with open('input.tsv', encoding = 'UTF-8') as source:
    head = next(source).rstrip('\n').split('\t')

if set(props) & set(head):
    print('output name clash with input name', file = sys.stderr)
    print('avoid clash with distinct prefix', file = sys.stderr)
    exit(1)

if form == 'flo':
    def format(x): return x
elif form == 'dec':
    def format(x): return '{:.4f}'.format(x)
elif form == 'by3':
    def format(x): return ceil(1000 * x)
elif form == 'by6':
    def format(x): return ceil(1000000 * x)
else:
    print('programming error - '
          'incomplete case analysis - '
          'please report', file = sys.stderr)
    exit(1)

# make it uniform so that even a single attribute is extracted as a tuple
# (maybe this should be another library - not sure - but almost sure)
def pick(head, keys):
    return ( itemgetter(*(map(head.index, keys)))
             if len(keys) > 1 else
             (lambda record, *, key = head.index(*keys): (record[key],))
             if keys else
             (lambda record: ()))

getgroup = pick(head, [ name for name, kind, sign in groupkeys ])
getcount = pick(head, countkeys)

def normalize(source):
    # must make lib_sortedtsv.process (and .save) deal with zero keys
    with open('output.tmp', mode = 'w', encoding = 'UTF-8') as out:
        print(*chain(props, head), sep = '\t', file = out)
        for k, group in groupby((line.rstrip('\n').split('\t')
                                 for line in source),
                                key = getgroup):
            records = list(group)
            totals = tuple(fsum(float(record[key])
                                for record in records)
                           for key in map(head.index, countkeys))
            for record in records:
                print(*chain((format(float(c)/t)
                              for c, t in zip(getcount(record), totals)),
                             record),
                      sep = '\t', file = out)

try:
    process('input.tsv', normalize, *groupkeys)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

os.rename('output.tmp', 'output.tsv')
