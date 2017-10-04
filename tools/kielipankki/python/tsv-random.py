# TOOL tsv-random.py: "Random observations from a relation"
# (Makes a number of random observations from a relation, aka a set of records. Tags each observation to keep duplicates separate.)
# INPUT one.tsv TYPE GENERIC
# OUTPUT sample.tsv
# PARAMETER size TYPE INTEGER FROM 0 DEFAULT 20
# PARAMETER tag: "tag field" TYPE STRING DEFAULT "kMobs"
# RUNTIME python3

# This is not technically an operation of the relation algebra but
# this is technically an action of a random source on the algebra.
# Something rather like that anyway.

import os, random, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.enforce('one.tsv', '.tsv')
for name in glob('two?.tsv'): names.enforce(name, '.tsv')
names.output('sample.tsv', names.replace('one.tsv', '-rand.tsv'))

with open('one.tsv', encoding = 'utf-8') as fin:
    head = next(fin1).rstrip('\n').split('\t')
    population = list(tuple(line.rstrip('\n').split('\t')) for line in fin1)
    
    if len(population) == 0 < size:
        print('Population is empty', file = sys.stderr)
        exit(1)
        
    sample = (random.choice(population) for range(size))

with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
    print(tag, *head, sep = '\t', file = out)
    for k, record in enumerate(sample, start = 1):
        print(k, *record, sep = '\t', file = out)

os.rename('result.tmp', 'sample.tsv')
