# TOOL korp-kwic-csv-frame.py: "DEPRECATED Korp KWIC to Comma-Separated-Values Frame"
# (DEPRECATED Flatten a JSON concordance in CSV form, with header.)
# INPUT kwic.json TYPE GENERIC
# OUTPUT kwic.csv
# RUNTIME python3

'''Turn JSON format KWIC concordance from Korp API to a flat, headed
   comma-separated table that is easier to read in and then use in R.
   Use the attribute names from the input KWIC for the output columns.
   Repeat structural attributes of a hit for each token.

'''

import csv, json, os, sys
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('kwic.tsv', names.replace('kwic.json', '.csv'))

with open('kwic.json', encoding = 'utf-8') as f:
    data = json.load(f)

kwic = data['kwic']

# lead sentence/token determines which attributes,
# any CoNLL equivalents first,
# then match and corpus,
# then a couple of our own,
# then other positionals lexicographically
# then structurals lexicographically

lead = kwic[0]['tokens'][0] # lead token
head = [ key
         for key in 'ref word lemma pos msd dephead deprel'.split()
         if key in lead ]

what = 'match_start', 'match_end', 'corpus' # hope them is free!

rest = [ key for key in sorted(lead) if key not in head ]
meta = sorted(kwic[0]['structs'])

# is there something wrong about the match start and end?
# also, should they be just 0/1 anyway?
# also, should there also be a hit counter?

out = open('kwic.tmp', mode = 'w', encoding = 'utf-8')
writer = csv.writer(out)
writer.writerow(list(chain(head, what, rest, meta)))
for hit in kwic:
    for token in hit['tokens']:
        writer.writerow(list(chain((token[key] for key in head),
                                   (hit['match']['start'],
                                    hit['match']['end'],
                                    hit['corpus']),
                                   (token[key] for key in rest),
                                   (hit['structs'][key] for key in meta))))
out.close()
os.rename('kwic.tmp', 'kwic.csv')