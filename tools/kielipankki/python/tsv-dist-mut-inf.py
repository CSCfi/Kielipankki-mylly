# TOOL tsv-dist-mut-inf.py: "Mutual information" (Mutual information of target variables, computed from a joint distribution, conditional on some variables, grouped by values of some variables)
# INPUT data.tsv: "Joint distribution" TYPE GENERIC (Relation containing joint proportions of some variables, need not be normalized to proportions)
# OUTPUT result.tsv
# PARAMETER dist: "Distribution field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER one1: "Target one field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER one2: "Target one field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER two1: "Target two field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER two2: "Target two field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER con1: "Condition field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER con2: "Condition field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER key1: "Grouping field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# PARAMETER key2: "Grouping field" TYPE COLUMN_SEL DEFAULT EMPTY ()
# RUNTIME python3

import os, sys
from collections import defaultdict
from math import fsum, log

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('result.tsv', 'mut-inf-{}'.format(base('data.tsv', '*.rel.tsv')),
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

# sorted to have canonical combination names in the result
ones = sorted(set(name for name in (one1, one2) if name not in ("EMPTY", "")))
twos = sorted(set(name for name in (two1, two2) if name not in ("EMPTY", "")))
cons = sorted(set(name for name in (con1, con2) if name not in ("EMPTY", "")))
keys = sorted(set(name for name in (key1, key2) if name not in ("EMPTY", "")))

class Pts: # so one can be "point-wise"
    def __init__(self, one, two, mix):
        self.one = one
        self.two = two
        self.mix = mix

freqs = defaultdict(lambda : defaultdict(lambda : Pts(defaultdict(float),
                                                      defaultdict(float),
                                                      defaultdict(float))))

try:
    with open('data.tsv', encoding = 'UTF-8') as data:
        head = next(data).rstrip('\n').split('\t')
        distx = head.index(dist)
        oneix = index(head, ones)
        twoix = index(head, twos)
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
                one = value(record, oneix)
                two = value(record, twoix)
                pts = freqs[key][con]
                pts.one[one] += freq
                pts.two[two] += freq
                pts.mix[one, two] += freq
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

# components of a pts have the same total

mutinf = dict((key, fsum((contotal/keytotal)
                         * fsum(p * log(p / (r * s))
                                for xy, f in pts.mix.items()
                                for x, y in [xy]
                                for g, h in [(pts.one[x], pts.two[y])]
                                for p, r, s in [(f/contotal,
                                                 g/contotal,
                                                 h/contotal)])
                         for con, pts in group.items()
                         for contotal in [sum(pts.one.values())]))
              for key, group in freqs.items()
              for keytotal in [sum(sum(pts.one.values())
                                   for con, pts in group.items())])

br = defaultdict(lambda : '({})') ; br[1] = '{}'
onename = br[len(ones)].format(','.join(ones))
twoname = br[len(twos)].format(','.join(twos))
conname = br[len(cons)].format(','.join(cons))
keyform = br[len(keys)]
keyname = keyform.format(','.join(keys))
log2 = log(2)

with open('result.tmp', mode = 'w', encoding = 'UTF-8') as out:
    print('var1', 'var2', 'cond',
          'wMmutinf', 'unit',
          'grouped', 'group',
          'dist',
          sep = '\t', file = out)
    for key, res in mutinf.items():
        keyval = keyform.format(','.join(key))
        print(onename, twoname, conname, res / log2, 'bits',
              keyname, keyval, dist,
              sep = '\t', file = out)
        print(onename, twoname, conname, res, 'nats',
              keyname, keyval, dist,
              sep = '\t', file = out)

os.rename('result.tmp', 'result.tsv')
