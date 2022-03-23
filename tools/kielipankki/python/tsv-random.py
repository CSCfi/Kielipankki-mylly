# TOOL tsv-random.py: "Random observations from a relation"
# (Makes a number of random observations from a relation, aka a set of records. Tags each observation to keep duplicates separate.)
# INPUT one.tsv TYPE GENERIC
# OUTPUT sample.tsv
# PARAMETER size TYPE INTEGER FROM 0 DEFAULT 20
# PARAMETER tag: "tag field" TYPE STRING DEFAULT "kMobs"

# This is not technically an operation of the relation algebra but
# this is technically an action of a random source on the algebra.
# Something rather like that anyway.

import os, random, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('sample.tsv', '{}-random'.format(base('one.tsv', '*.rel.tsv')),
     ext = 'rel.tsv')

def checktag(tag, head):
    if tag in head:
        print("tag name already in use:", repr(tag),
              file = sys.stderr)
        print("choose any that is not one of these:",
              *map(repr, head), sep = '\n', file = sys.stderr)
        exit(1)

with open('one.tsv', encoding = 'utf-8') as fin:
    head = next(fin).rstrip('\n').split('\t')
    checktag(tag, head)
    population = list(tuple(line.rstrip('\n').split('\t')) for line in fin)
    
    if len(population) == 0 < size:
        print('Population is empty', file = sys.stderr)
        exit(1)
        
    sample = (random.choice(population) for _ in range(size))

with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
    print(tag, *head, sep = '\t', file = out)
    for k, record in enumerate(sample, start = 1):
        print(k, *record, sep = '\t', file = out)

os.rename('result.tmp', 'sample.tsv')
