# TOOL tsv-ngram.py: "N-grams" ()
# INPUT input.tsv TYPE GENERIC
# OUTPUT output.tsv
# PARAMETER asen TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER atok TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER gsiz TYPE INTEGER FROM 1 TO 5 DEFAULT 2
# PARAMETER attr1 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr2 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr3 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr4 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr5 TYPE COLUMN_SEL DEFAULT EMPTY
# RUNTIME python3

# asen is for grouping sentences input and output
# atok is for ordering tokens within input sentence
# output grams are numbered within sentence

import os, sys
from itertools import chain, groupby
from operator import itemgetter

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import name, base
from lib_sortedtsv import process

name('output.tsv', base('input.tsv', '*.rel.tsv'),
     ins = '{}-gram'.format(gsiz),
     ext = 'rel.tsv')

keys = tuple(set(key for key in (attr1, attr2, attr3, attr4, attr5)
                 if key not in ('EMPTY', '')))

if not keys:
    print('grams must consist of some attributes', file = sys.stderr)
    exit(1)

reskeys = tuple('w{}{}'.format(word + 1, key)
                for word in range(gsiz)
                for key in keys)

with open('input.tsv', encoding = 'UTF-8') as source:
    head = next(source).rstrip('\n').split('\t')

# make it uniform so that even a single attribute is extracted as a tuple
data = ( itemgetter(*(head.index(key) for key in keys))
         if len(keys) > 1
         else lambda record, *, key = head.index(*keys): (record[key],) )

def window(source):
    with open('output.tmp', mode = 'w', encoding = 'UTF-8') as out:
        print(asen, 'kMgram', 'end', *reskeys, sep = '\t', file = out)
        for k, group in groupby((line.rstrip('\n').split('\t')
                                 for line in source),
                                key = itemgetter(head.index(asen))):
            sen = list(map(data, group))
            end = len(sen) - gsiz + 1
            for t, gram in ((1 + t, sen[t:t + gsiz])
                            for t in range(end)):
                print(k, t, (t == 1) + 2 * (t == end),
                      *chain.from_iterable(gram),
                      sep = '\t', file = out)

# untested sanity checks follow

if asen in reskeys:
    print('sentence attribute', asen, 'is one of', *reskeys,
          file = sys.stderr)
    exit(1)

if asen == 'kMgram':
    print('sentence attribute', asen, 'is kMgram',
          file = sys.stderr)
    exit(1)

if asen == 'end':
    print('sentence attribute', asen, 'is end',
          file = sys.stderr)
    exit(1)

try:
    process('input.tsv', window, asen, atok)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

os.rename('output.tmp', 'output.tsv')
