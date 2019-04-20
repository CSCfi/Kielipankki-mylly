# TOOL kwic-as-tsv.py: "KWIC as Rel.TSV"
# (Write Korp JSON-form concordance as two TSV files: tokens with their positional annotations as one relation, structural annotations as another. Both files contain a sentence counter on which they can be easily joined.)
# INPUT kwic.json TYPE GENERIC
# OUTPUT tokens.tsv
# OUTPUT meta.tsv
# RUNTIME python3

import json, os, sys
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('tokens.tsv', base('kwic.json', '*.korp.json'),
     ins = 'data',
     ext = 'rel.tsv')
name('meta.tsv', base('kwic.json', '*.korp.json'),
     ins = 'meta',
     ext = 'rel.tsv')

with open('kwic.json', encoding = 'utf-8') as f:
    data = json.load(f)

kwic = data['kwic']

# lead sentence/token determines which positional attributes

head = list(kwic[0]['tokens'][0])

# also: kMmatch (0/1), kMsen (counter, also in meta), kMtok (counter
# within kMsen) though kMmatch may want to be bMmatch or some such
# some day (Boolean?)  the new naming scheme with these prefixen
# indicates types to ODS-maker and such

# if the JSON concordance originates in Mylly, it also records the
# page origin relative to the whole concordance as data['M']['origin']
# otherwise assume kMsen is to start at 0

origin = data.get('M', {}).get('origin', 0)

with open('tokens.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('kMmatch', 'kMsen', 'kMtok', *head, sep = '\t', file = out)
    for j, hit in enumerate(kwic, start = origin):
        for k, token in enumerate(hit['tokens']):
            m = hit['match']
            print(int(m['start'] <= k < m['end']),
                  j, k,
                  *(token[key] for key in head),
                  sep = '\t', file = out)
        
os.rename('tokens.tmp', 'tokens.tsv')

meta = list(kwic[0]['structs'])
# also: kMsen (counter, also in tokens), kMstart, kMend, sMcorpus
# now naming also "start", "end", and "corpus" with Mylly prefixes.

with open('meta.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('kMsen', 'kMstart', 'kMend', 'sMcorpus', *meta, sep = '\t', file = out)
    for j, hit in enumerate(kwic, start = origin):
        m, c, data = hit['match'], hit['corpus'], hit['structs']
        print(j, m['start'], m['end'], c, *(data[key] for key in meta),
              sep = '\t', file = out)

os.rename('meta.tmp', 'meta.tsv')
