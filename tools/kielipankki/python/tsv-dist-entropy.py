# TOOL tsv-dist-entropy.py: "Entropy" (Entropy of target variables, computed from a joint distribution, conditional on some variables, grouped by values of some variables)
# INPUT data.tsv: "Joint distribution" TYPE GENERIC (Relation containing joint proportions of some variables, need not be normalized to proportions)
# OUTPUT result.tsv
# PARAMETER dist: "Distribution field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER val1: "Target field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER val2: "Target field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER val3: "Target field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER val4: "Target field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER con1: "Condition field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER con2: "Condition field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER key1: "Grouping field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER key2: "Grouping field" TYPE COLUMN_SEL DEFAULT EMPTY ()

import os, sys
from collections import defaultdict
from math import fsum, log

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('result.tsv', 'entropy-{}'.format(base('data.tsv', '*.rel.tsv')),
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

# sorted to have canonical combination names in the result
vals = sorted(set(name for name in (val1, val2,
                                    val3, val4) if name not in ("EMPTY", "")))
cons = sorted(set(name for name in (con1, con2) if name not in ("EMPTY", "")))
keys = sorted(set(name for name in (key1, key2) if name not in ("EMPTY", "")))

freqs = defaultdict(lambda : defaultdict(lambda : defaultdict(float)))

try:
    with open('data.tsv', encoding = 'UTF-8') as data:
        head = next(data).rstrip('\n').split('\t')
        distx = head.index(dist)
        valix = index(head, vals)
        conix = index(head, cons)
        keyix = index(head, keys)
        for line in data:
            record = line.rstrip('\n').split('\t')
            freq = float(record[distx])
            if freq < 0.0:
                raise ValueError('proportion cannot be negative: {}'
                                 .format(freq))
            elif freq > 0.0:
                key = value(record, keyix)
                con = value(record, conix)
                val = value(record, valix)
                freqs[key][con][val] += freq
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

entropy = dict((key, fsum((contotal/keytotal)
                          * fsum(- p * log(p)
                                 for f in dis.values()
                                 for p in [f/contotal])
                          for con, dis in group.items()
                          for contotal in [sum(dis.values())]))
               for key, group in freqs.items()
               for keytotal in [sum(sum(dis.values())
                                    for con, dis in group.items())])

br = defaultdict(lambda : '({})') ; br[1] = '{}'
valname = br[len(vals)].format(','.join(vals))
conname = br[len(cons)].format(','.join(cons))
kf = br[len(keys)]
keyname = kf.format(','.join(keys))
log2 = log(2)

with open('result.tmp', mode = 'w', encoding = 'UTF-8') as out:
    print('variable', 'condition', 'wMentropy', 'unit',
          'grouped', 'group',
          'count',
          sep = '\t', file = out)
    for key, res in entropy.items():
        keyval = kf.format(','.join(key))
        print(valname, conname, res / log2, 'bits', keyname, keyval, dist,
              sep = '\t', file = out)
        print(valname, conname, res, 'nats', keyname, keyval, dist,
              sep = '\t', file = out)

os.rename('result.tmp', 'result.tsv')
