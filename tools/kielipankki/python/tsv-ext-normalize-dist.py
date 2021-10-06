# TOOL tsv-ext-normalize-dist.py: "Add normalized distribution" (Extend relation with a normalized distribution)
# INPUT data.tsv TYPE GENERIC
# OUTPUT result.tsv
# PARAMETER dist: "Input distribution attribute" TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER norm: "Output distribution attribute" TYPE STRING
# IMAGE comp-16.04-mylly
# RUNTIME python3

import os, sys
from math import fsum, isfinite

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('result.tsv', base('data.tsv', '*.rel.tsv'),
     ins = 'ext-norm',
     ext = 'rel.tsv')

try:
    with open('data.tsv', encoding = 'UTF-8') as data:
        head = next(data).rstrip('\n').split('\t')
        if norm in head:
            raise ValueError('attribute in use:'.format(norm))
        ix = head.index(dist)
        old = [ line.rstrip('\n').split('\t') for line in data ]
        
        def freq(value):
            weight = float(value)
            if weight < 0:
                raise ValueError('proportion cannot be negative: {}'
                                 .format(value))
            if not isfinite(weight):
                raise ValueError('proportion must be finite: {}'
                                 .format(value))
            return weight

        new = [ freq(record[ix]) for record in old ]
        total = sum(new)

        if total == 0.0:
            raise ValueError('cannot normalize total 0.0 to 1.0')

except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

with open('result.tmp', mode = 'w', encoding = 'UTF-8') as out:
    print(norm, *head, sep = '\t', file = out)
    for weight, rest in zip(new, old):
        print(weight/total, *rest, sep = '\t', file = out)

os.rename('result.tmp', 'result.tsv')
