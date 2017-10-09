# TOOL tsv-image.py: "Image of composed relation"
# (Make an image where the records consist of the non-shared attributes of the records of the first relation matching some records in the second relation.)
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
names.output('result.tsv', names.replace('one.tsv', '-image.tsv'))

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

        two = {
            value(record, midrix)
            for line in fin2
            for record in [line.rstrip('\n').split('\t')]
        }

        result = {
            value(record, leftix)
            for line in fin1
            for record in [line.rstrip('\n').split('\t')]
            if value(record, midlix) in two
        }

with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
    print(*value(onehead, leftix),
          sep = '\t', file = out)
    for record in result:
        print(*record, sep = '\t', file = out)

os.rename('result.tmp', 'result.tsv')
