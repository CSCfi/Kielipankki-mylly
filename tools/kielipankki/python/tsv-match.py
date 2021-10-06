# TOOL tsv-match.py: "Match another relation"
# (Makes that part of the first relation that matches the second relation.)
# INPUT one.tsv TYPE GENERIC
# INPUT two.tsv TYPE GENERIC
# OUTPUT match.tsv
# IMAGE comp-16.04-mylly
# RUNTIME python3

import sys, os

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('match.tsv', base('one.tsv', '*.rel.tsv'),
     ins = 'match.{}'.format(base('two.tsv', '*.rel.tsv')),
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def share(head, head2): return tuple(set(head) & set(head2))
def other(head, names): return tuple(set(head) - set(names))
def value(record, ks): return tuple(record[k] for k in ks)

with open('one.tsv', encoding = 'utf-8') as fin1:
    with open('two.tsv', encoding = 'utf-8') as fin2:
        onehead = next(fin1).rstrip('\n').split('\t')
        twohead = next(fin2).rstrip('\n').split('\t')
        
        onix = index(onehead, share(onehead, twohead))
        twix = index(twohead, share(onehead, twohead))
        
        keys = set(value(line.rstrip('\n').split('\t'), twix)
                   for line in fin2)
        
        with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
            print(*onehead, sep = '\t', file = out)
            for record in (line.rstrip('\n').split('\t')
                           for line in fin1):
                if value(record, onix) in keys:
                    print(*record, sep = '\t', file = out)

os.rename('result.tmp', 'match.tsv')
