# TOOL kwic-2gram.py: "KWIC 2-grams in TSV"
# (Two-grams from a Korp JSON-form concordance in a TSV file. Selected positional attributes are suffixed with 1 and 2 for consecutive tokens inside sentences. Sentence and token counters, kMsen and kMtok, are added to identify each occurrence.)
# INPUT kwic.json TYPE GENERIC
# OUTPUT grammata.tsv
# PARAMETER          attr0 TYPE STRING
# PARAMETER OPTIONAL attr1 TYPE STRING
# PARAMETER OPTIONAL attr2 TYPE STRING
# PARAMETER OPTIONAL attr3 TYPE STRING
# RUNTIME python3

import json, os, sys
from itertools import chain, count

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('grammata.tsv', names.replace('kwic.json', '-2g.tsv'))

with open('kwic.json', encoding = 'utf-8') as f:
    data = json.load(f)

kwic = data['kwic']

# head = list(kwic[0]['tokens'][0]) # lead token
# should make some relational sanity checks here
head = tuple(filter(None, (attr0, attr1, attr2, attr3)))

# also: kMsen (counter, also in meta), kMtok (counter within kMsen)
# not sure if there should be kMmatch or bMmatch or some such some day (Boolean?)
# the new naming scheme with these prefixen indicates types to ODS-maker and such

with open('grammata.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('kMsen', 'kMtok',
          *chain(map('{}1'.format, head),
                 map('{}2'.format, head)),
          sep = '\t',
          file = out)
    for j, hit in enumerate(kwic):
        first = iter(hit['tokens'])
        second = iter(hit['tokens'])
        next(second, None)
        for k, tic, toc in zip(count(), first, second):
            # m = hit['match'] # int(m['start'] <= k < m['end']),
            print(j, k,
                  *chain((tic[key] for key in head),
                         (toc[key] for key in head)),
                  sep = '\t',
                  file = out)
        
os.rename('grammata.tmp', 'grammata.tsv')

# Should start kMsen from Start, right?
#
# meta = list(kwic[0]['structs'])
# also: kMsen (counter, also in tokens), Start, End, Corpus
# though not sure whether Start, End, Corpus are safe or might also occur
# as positional in some corpus or other - are they safe? with the Cap?
#
# with open('meta.tmp', mode = 'w', encoding = 'utf-8') as out:
#    print('kMsen', 'Start', 'End', 'Corpus', *meta, sep = '\t', file = out)
#    for j, hit in enumerate(kwic):
#        m, c, data = hit['match'], hit['corpus'], hit['structs']
#        print(j, m['start'], m['end'], c, *(data[key] for key in meta),
#              sep = '\t', file = out)
