# TOOL korp-kwic-to-tsv.py: "Korp KWIC from JSON to IANA TSV"
# (Flatten a JSON concordance in IANA TSV form, with a header of unique field names. Tokens with positional annotations are saved in one file, structural annotations in another, both sharing a sentence identifier so that the files can be joined.)
# INPUT kwic.json TYPE GENERIC
# OUTPUT tokens.tsv
# OUTPUT meta.tsv
# RUNTIME python3

'''[Fix this comment - there are two files now.]
   Turn JSON format KWIC concordance from Korp API to a flat, headed
   tab-separated table that is easier to read in and then use in R.
   Use the attribute names from the input KWIC for the output columns.
   Repeat structural attributes of a hit for each token.

'''

import json, os, sys
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('tokens.tsv', names.replace('kwic.json', '-tokens.tsv'))
names.output('meta.tsv', names.replace('kwic.json', '-meta.tsv'))

with open('kwic.json', encoding = 'utf-8') as f:
    data = json.load(f)

kwic = data['kwic']

# lead sentence/token determines which attributes,

head = list(kwic[0]['tokens'][0]) # lead token
# also: _match (0/1), _hit (counter, also in meta)

# is there something wrong about match start and end?

with open('tokens.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('_match', '_sen', '_tok', *head, sep = '\t', file = out)
    for j, hit in enumerate(kwic):
        for k, token in hit['tokens']:
            m = hit['match']
            print(int(m['start'] <= k <= m['end']),
                  j, k,
                  *(token[key] for key in head),
                  sep = '\t', file = out)
        
os.rename('tokens.tmp', 'tokens.tsv')

meta = list(kwic[0]['structs'])
# also: _hit (counter, also in head), _start, _end, _corpus

with open('meta.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('_hit', '_start', '_end', '_corpus', *meta, sep = '\t', file = out)
    for j, hit in enumerate(kwic):
        m, c = hit['match'], hit['corpus']
        print(j, m['start'], m['end'], c, *(token[key] for key in meta),
              sep = '\t', file = out)

os.rename('meta.tmp', 'meta.tsv')
