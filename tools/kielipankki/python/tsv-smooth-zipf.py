# TOOL tsv-smooth-zipf.py: "Extend Zipfian TSV with smoothed species count"
# (Extend a map of observation count to the species count with a linearly smoothed species count, from Sampson)
# INPUT counts.tsv TYPE GENERIC
# OUTPUT smooth.tsv
# PARAMETER observations TYPE STRING DEFAULT "observations"
# PARAMETER species TYPE STRING DEFAULT "species"
# PARAMETER smooth TYPE STRING DEFAULT "species1"
# RUNTIME python3

import os, sys
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('smooth.tsv', base('counts.tsv', '*.rel.tsv'),
     ins = 'smooth',
     ext = 'rel.tsv')

with open('counts.tsv') as counts:
    head = next(counts).rstrip('\n').split('\t')
    OBS = head.index(observations)
    SPE = head.index(species)
    data = sorted((int(record[OBS]),
                   int(record[SPE]),
                   record)
                  for record in (line.rstrip('\n').split('\t')
                                 for line in counts))

ps = (obs for obs, spe, rec in data)
ns = (spe for obs, spe, rec in data)
qs = (obs for obs, spe, rec in data)

ps = chain([0], ps)

pen, _, _ = data[-2]
ult, _, _ = data[-1]
qs = chain(qs, [2*ult - pen])
next(qs)

zs = (2*n/(q - p) for p, n, q in zip(ps, ns, qs))
rs = (rec for obs, spe, rec in data)

with open('smooth.tmp', mode = 'w') as out:
    print(smooth, *head, sep = '\t', file = out)
    for z, r in zip(zs, rs):
        print(z, *r, sep = '\t', file = out)

os.rename('smooth.tmp', 'smooth.tsv')
