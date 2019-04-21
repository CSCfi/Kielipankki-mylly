# TOOL tsv-ext-count.py: "Extend relation with frequency"
# (Extend each record with the frequency of a selected attribute combination, by default in the relation itself but optionally in another relation. The prefix cM in count name indicates numeric type to some tools.)
# INPUT target.tsv: "Relation to extend" TYPE GENERIC
# INPUT OPTIONAL source.tsv: "Relation to count in" TYPE GENERIC
# OUTPUT result.tsv
# PARAMETER tfreq: "frequency" TYPE STRING DEFAULT "cMfreq"
# PARAMETER attr1: "attribute 1" TYPE COLUMN_SEL
# PARAMETER OPTIONAL attr2: "attribute 2" TYPE COLUMN_SEL
# PARAMETER OPTIONAL attr3: "attribute 3" TYPE COLUMN_SEL
# PARAMETER OPTIONAL sfreq: "count (if already counted)" TYPE COLUMN_SEL
# RUNTIME python3

# Cannot be a mere counting projection or a join with one because
# needs to be able to observe zero occurrences. Glad you asked.
# However, other combinations in other relation - not observed!

from collections import Counter

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('result.tsv', base('target.tsv', '*.rel.tsv'),
     ins = 'count',
     ext = 'rel.tsv')

# hope that chipster allows COLUMN_SEL from the other relation! aha,
# but both relations must have the attributes that are being counted!

comb = tuple(set(name for name in (attr1, attr2, attr3)
                 if name not in ("EMPTY", "")))

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

with open('target.tsv', encoding = 'utf-8') as fint:
    thead = next(fint).rstrip('\n').split('\t')

if tfreq in thead:
    print('new name {} is already in use:'.format(repr(tfreq)),
          file = sys.stderr)
    print(*thead, file = sys.stderr)
    exit(1)

with open(( 'source.tsv' if os.path.exists('source.tsv')
            else 'target.tsv' ),
          encoding = 'utf-8') as fins:
    shead = next(fins).rstrip('\n').split('\t')
    six = index(shead, comb)
    if sfreq in ("EMPTY", ""):
        counts = Counter(value(line.rstrip('\n').split('\t'), six)
                         for line in fins)
    else:
        wx = shead.index(sfreq)
        counts = dict((value(record, six), int(record[wx]))
                      for line in fins
                      for record in [line.rsplit('\n').split('\t')])

with open('target.tsv', encoding = 'utf-8') as fin:
    with open('result.tmp', mode = 'w', encoding = 'utf-8') as out:
        next(fin)
        print(tfreq, *thead, sep = '\t', file = out)
        tix = index(thead, comb)
        for line in fin:
            record = line.rstrip('\n').split('\t')
            print(counts.get(value(record, tix), 0),
                  *record, sep = '\t', file = out)

os.rename('result.tmp', 'result.tsv')
