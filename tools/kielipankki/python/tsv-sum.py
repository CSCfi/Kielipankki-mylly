# TOOL tsv-sum.py: "Sum of relations"
# (Makes sum aka disjoint union of relations that have the same type modulo optional tag field. Tags or re-tags each record to separate the sources.)
# INPUT input0.tsv TYPE GENERIC
# INPUT OPTIONAL input1.tsv TYPE GENERIC
# INPUT OPTIONAL input2.tsv TYPE GENERIC
# INPUT OPTIONAL input3.tsv TYPE GENERIC
# INPUT OPTIONAL input4.tsv TYPE GENERIC
# INPUT OPTIONAL input5.tsv TYPE GENERIC
# INPUT OPTIONAL input6.tsv TYPE GENERIC
# INPUT OPTIONAL input7.tsv TYPE GENERIC
# INPUT OPTIONAL input8.tsv TYPE GENERIC
# INPUT OPTIONAL input9.tsv TYPE GENERIC
# INPUT OPTIONAL inputA.tsv TYPE GENERIC
# INPUT OPTIONAL inputB.tsv TYPE GENERIC
# INPUT OPTIONAL inputC.tsv TYPE GENERIC
# INPUT OPTIONAL inputD.tsv TYPE GENERIC
# INPUT OPTIONAL inputE.tsv TYPE GENERIC
# INPUT OPTIONAL inputF.tsv TYPE GENERIC
# OUTPUT sum.tsv
# PARAMETER tag: "tag field" TYPE STRING DEFAULT "kMtag"

from collections import defaultdict
from itertools import count
from glob import glob
import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

for rest in glob('input?.tsv'): base(rest, '*.rel.tsv')
name('sum.tsv', base('input0.tsv', '*.rel.tsv'),
     ins = 'sum',
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

def checktype(ones, twos):
    oneset, twoset = set(ones), set(twos)
    if oneset == twoset: return
    print('union-incompatible heads', file = sys.stderr)
    print('only in first:', *(oneset - twoset), file = sys.stderr)
    print('only in second:', *(twoset - oneset), file = sys.stderr)
    print('in both:', *(oneset & twoset), file = sys.stderr)
    exit(1)

def mod(names):
    '''modulo tag field'''
    return [ name for name in names if name != tag ]

with open('sum.tmp', mode = 'w', encoding = 'utf-8') as out:
    onehead = next(open('input0.tsv', encoding = 'UTF-8')).rstrip('\n').split('\t')
    print(tag, *mod(onehead), sep = '\t', file = out)

    tic = count(start = 1)
    for inf in sorted(glob('input?.tsv')):
        with open(inf, encoding = 'utf-8') as fin:
            twohead = next(fin).rstrip('\n').split('\t')
            checktype(mod(onehead), mod(twohead))
            twindex = index(twohead, mod(onehead))

            if tag in twohead:
                # relation already has tags
                def get(record, *, k = twohead.index(tag)): return record[k]
            else:
                # provide constant tag for relation
                def get(record): return '1'
            
            tac = defaultdict(lambda : next(tic))
            for t, record in ((tac[get(record)], value(record, twindex))
                              for line in fin
                              for record in [line.rstrip('\n').split('\t')]):
                print(t, *record, sep = '\t', file = out)

os.rename('sum.tmp', 'sum.tsv')
