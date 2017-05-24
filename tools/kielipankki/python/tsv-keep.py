# TOOL tsv-keep.py: "Keep given TSV attributes"
# (Keep the given attributes. Produce counts if given a name for count attribute. Prefix cM of the default cMcount indicates numeric type for some tools.)
# INPUT wide.tsv TYPE GENERIC
# OUTPUT narrow.tsv
# PARAMETER OPTIONAL count TYPE STRING DEFAULT "cMcount"
# PARAMETER          keep0 TYPE STRING
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
# RUNTIME python3

from collections import Counter
import os

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('narrow.tsv', names.replace('wide.tsv', '-keep.tsv'))

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

keep = set(filter(None, (keep0, keep1, keep2, keep3,
                         keep4, keep5, keep6, keep7,
                         keep8, keep9, keepA, keepB,
                         keepC, keepD, keepE, keepF)))

with open('wide.tsv') as wide:
    head = next(wide).rstrip('\n').split('\t')
    take = index(head, keep)
    them = Counter(value(line.rstrip('\n').split('\t'), take)
                   for line in wide)

# should check that count not in kept (that be an error)

with open('narrow.tmp', mode = 'w', encoding = 'utf-8') as out:
    if count:
        print(count, *value(head, take), sep = '\t', file = out)
        for it in them:
            print(them[it], *it, sep = '\t', file = out)
    else:
        print(*value(head, take), sep = '\t', file = out)
        for it in them:
            print(*it, sep = '\t', file = out)

os.rename('narrow.tmp', 'narrow.tsv')
