# TOOL tsv-intersection.py: "Intersection of relations"
# (Makes intersection of relations of same type represented as TSV files)
# INPUT one.tsv TYPE GENERIC
# INPUT OPTIONAL two1.tsv TYPE GENERIC
# INPUT OPTIONAL two2.tsv TYPE GENERIC
# INPUT OPTIONAL two3.tsv TYPE GENERIC
# INPUT OPTIONAL two4.tsv TYPE GENERIC
# OUTPUT intersection.tsv
# RUNTIME python3

from glob import glob
import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

for name in glob('two?.tsv'): base(name, '*.rel.tsv')
name('intersection.tsv', base('one.tsv', '*.rel.tsv'),
     ins = 'intersection',
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def share(head, head2): return tuple(set(head) & set(head2))
def other(head, names): return tuple(set(head) - set(names))
def value(record, ks): return tuple(record[k] for k in ks)

def checktype(ones, twos):
    oneset, twoset = set(ones), set(twos)
    if oneset == twoset: return
    print('union-incompatible heads', file = sys.stderr)
    print('only in first:', *(oneset - twoset), file = sys.stderr)
    print('only in second:', *(twoset - oneset), file = sys.stderr)
    print('in both:', *(oneset & twoset), file = sys.stderr)
    exit(1)    

with open('one.tsv', encoding = 'utf-8') as fin1:
    onehead = next(fin1).rstrip('\n').split('\t')
    result = set(tuple(line.rstrip('\n').split('\t')) for line in fin1)
    for two in glob('two?.tsv'):
        with open(two, encoding = 'utf-8') as fin2:
            twohead = next(fin2).rstrip('\n').split('\t')
            checktype(onehead, twohead)
            twindex = index(twohead, onehead)
            records = (value(line.rstrip('\n').split('\t'), twindex)
                       for line in fin2)
            result.intersection_update(records)

with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
    print(*onehead, sep = '\t', file = out)
    for record in result:
        print(*record, sep = '\t', file = out)

os.rename('result.tmp', 'intersection.tsv')
