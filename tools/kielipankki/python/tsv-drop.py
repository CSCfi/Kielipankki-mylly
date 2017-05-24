# TOOL tsv-drop.py: "Drop given TSV attributes"
# (Drop the given attributes. Produce counts if given a name for count attribute. Prefix cM of the default cMcount indicates numeric type for some tools.)
# INPUT wide.tsv TYPE GENERIC
# OUTPUT narrow.tsv
# PARAMETER OPTIONAL count TYPE STRING DEFAULT "cMcount"
# PARAMETER          drop0 TYPE STRING
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
# RUNTIME python3

from collections import Counter
import os

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('narrow.tsv', names.replace('wide.tsv', '-drop.tsv'))

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

drop = set(filter(None, (drop0, drop1, drop2, drop3,
                         drop4, drop5, drop6, drop7,
                         drop8, drop9, dropA, dropB,
                         dropC, dropD, dropE, dropF)))

with open('wide.tsv') as wide:
    head = next(wide).rstrip('\n').split('\t')
    take = index(head, set(head) - drop)
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
