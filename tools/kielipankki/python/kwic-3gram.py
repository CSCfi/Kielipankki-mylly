# TOOL kwic-3gram.py: "KWIC 3-grams as relation"
# (Write 3-grams from a Korp JSON-form concordance as a TSV relation file. One or more positional attributes are suffixed with 1, 2, and 3 for consecutive tokens in a sentence. Sentence and token counters, kMsen and kMtok, identify each occurrence.)
# INPUT kwic.json: "Concordance file" TYPE GENERIC
#     (A KWIC concordance in a Korp JSON file)
# OUTPUT grammata.tsv
# PARAMETER          attr0: "Attribute" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     msd: msd
# ] (An attribute to include for each token in a 3-gram)
# PARAMETER OPTIONAL attr1: "Attribute" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     msd: msd
# ]
# PARAMETER OPTIONAL attr2: "Attribute" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     msd: msd
# ]
# PARAMETER OPTIONAL attr3: "Attribute" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     msd: msd
# ]
# PARAMETER OPTIONAL attr4: "Attribute" TYPE STRING
# PARAMETER OPTIONAL attr5: "Attribute" TYPE STRING
# PARAMETER OPTIONAL attr6: "Attribute" TYPE STRING
# PARAMETER OPTIONAL attr7: "Attribute" TYPE STRING

import json, os, sys
from itertools import chain, count

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('grammata.tsv', base('kwic.json', '*.korp.json'),
     ins = '3-gram',
     ext = 'rel.tsv')

with open('kwic.json', encoding = 'utf-8') as f:
    data = json.load(f)

kwic = data['kwic']

# head = list(kwic[0]['tokens'][0]) # lead token
# should make some relational sanity checks here
head = tuple(filter(None, (attr0, attr1, attr2, attr3,
                           attr4, attr5, attr6, attr7)))

# some sanity check
if len(head) > len(set(head)):
    print('duplicate attribute names:', *head,
          sep = '\n',
          file = sys.stderr)
    exit(1)

# also: kMsen (counter, also in meta), kMtok (counter within kMsen)
# not sure if there should be kMmatch or bMmatch or some such some day (Boolean?)
# the new naming scheme with these prefixen indicates types to ODS-maker and such

with open('grammata.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('kMsen', 'kMtok',
          *chain(map('{}1'.format, head),
                 map('{}2'.format, head),
                 map('{}3'.format, head)),
          sep = '\t',
          file = out)
    for j, hit in enumerate(kwic):
        first = iter(hit['tokens'])
        second = iter(hit['tokens'])
        third = iter(hit['tokens'])
        next(second, None)
        next(third, None)
        next(third, None)
        for k, tic, tac, toc in zip(count(), first, second, third):
            # m = hit['match'] # int(m['start'] <= k < m['end']),
            print(j, k,
                  *chain((tic[key] for key in head),
                         (tac[key] for key in head),
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
