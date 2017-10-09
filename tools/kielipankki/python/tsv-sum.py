# TOOL tsv-sum.py: "Sum of relations"
# (Makes sum aka disjoint union of relations of same type. Tags each record to separate the sources.)
# INPUT one.tsv TYPE GENERIC
# INPUT OPTIONAL two1.tsv TYPE GENERIC
# INPUT OPTIONAL two2.tsv TYPE GENERIC
# INPUT OPTIONAL two3.tsv TYPE GENERIC
# INPUT OPTIONAL two4.tsv TYPE GENERIC
# OUTPUT sum.tsv
# PARAMETER tag: "tag field" TYPE STRING DEFAULT "kMtag"
# RUNTIME python3

from itertools import chain
from glob import glob
import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.enforce('one.tsv', '.tsv')
for name in glob('two?.tsv'): names.enforce(name, '.tsv')
names.output('sum.tsv', names.replace('one.tsv', '-sum.tsv'))

def index(head, names): return tuple(map(head.index, names))
def share(head, head2): return tuple(set(head) & set(head2))
def other(head, names): return tuple(set(head) - set(names))
def value(record, ks): return tuple(record[k] for k in ks)

def checktag(tag, head):
    if tag in head:
        print("tag name already in use:", repr(tag),
              file = sys.stderr)
        print("choose any that is not one of these:",
              *map(repr, head), sep = '\n', file = sys.stderr)
        exit(1)

def checktype(ones, twos):
    oneset, twoset = set(ones), set(twos)
    if oneset == twoset: return
    print('union-incompatible heads', file = sys.stderr)
    print('only in first:', *(oneset - twoset), file = sys.stderr)
    print('only in second:', *(twoset - oneset), file = sys.stderr)
    print('in both:', *(oneset & twoset), file = sys.stderr)
    exit(1)    

with open('sum.tmp', mode = 'w', encoding = 'utf-8') as out:
    with open('one.tsv', encoding = 'utf-8') as fin1:
        onehead = next(fin1).rstrip('\n').split('\t')
        checktag(tag, onehead)
        print(tag, *onehead, sep = '\t', file = out)
        for record in (line.rstrip('\n').split('\t') for line in fin1):
            # overkill
            print(1, *record, sep = '\t', file = out)
        for k, two in enumerate(glob('two?.tsv'), start = 2):
            with open(two, encoding = 'utf-8') as fin2:
                twohead = next(fin2).rstrip('\n').split('\t')
                checktype(onehead, twohead)
                twindex = index(twohead, onehead)
                for record in (value(line.rstrip('\n').split('\t'), twindex)
                               for line in fin2):
                    # not overkill
                    print(k, *record, sep = '\t', file = out)

os.rename('sum.tmp', 'sum.tsv')
