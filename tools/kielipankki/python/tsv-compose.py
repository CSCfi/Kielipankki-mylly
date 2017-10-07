# TOOL tsv-compose.py: "Composition of two relations"
# (Make a composed relation whose records consists of the non-shared attributes of the matching records.)
# INPUT one.tsv TYPE GENERIC
# INPUT two.tsv TYPE GENERIC
# OUTPUT result.tsv
# RUNTIME python3

import os, sys
from collections import defaultdict

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.enforce('one.tsv', '.tsv')
names.enforce('two.tsv', '.tsv')
names.output('result.tsv', names.replace('one.tsv', '-compose.tsv'))

def index(head, names): return tuple(map(head.index, names))
def share(head, head2): return tuple(set(head) & set(head2))
def other(head, names): return tuple(set(head) - set(names))
def value(record, ks): return tuple(record[k] for k in ks)

with open('one.tsv', encoding = 'utf-8') as fin1:
    with open('two.tsv', encoding = 'utf-8') as fin2:
        onehead = next(fin1).rstrip('\n').split('\t')
        twohead = next(fin2).rstrip('\n').split('\t')
        leftix = index(onehead, other(onehead, share(onehead, twohead)))
        midlix = index(onehead, share(onehead, twohead))
        midrix = index(twohead, share(onehead, twohead))
        riteix = index(twohead, other(twohead, share(onehead, twohead)))

        one = defaultdict(list)
        for line in fin1:
            record = line.rstrip('\n').split('\t')
            one[value(record, midlix)].append(value(record, leftix))

        result = {
            (left + rite) for line in fin2
            for record in [line.rstrip('\n').split('\t')]
            for left in one.get(value(record, midrix), [])
            for rite in [value(record, riteix)]
        }

with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
    print(*(value(onehead, leftix) + value(twohead, riteix)),
          sep = '\t', file = out)
    for record in result:
        print(*record, sep = '\t', file = out)

os.rename('result.tmp', 'result.tsv')
