# TOOL kwic-dep.py: "KWIC dependency triples in TSV"
# (Dependents and their heads, together with their dependency relation from a suitably annotated Korp JSON-form concordance in a TSV file. Selected positional attributes are suffixed with 1 for the dependent and 2 for the head. Sentence and token counters, kMsen and kMtok, are added to identify each dependent occurrence.)
# INPUT kwic.json TYPE GENERIC
# OUTPUT triplaux.tsv
# PARAMETER          attr0 TYPE STRING
# PARAMETER OPTIONAL attr1 TYPE STRING
# PARAMETER OPTIONAL attr2 TYPE STRING
# PARAMETER OPTIONAL attr3 TYPE STRING
# PARAMETER OPTIONAL attr4 TYPE STRING
# PARAMETER OPTIONAL attr5 TYPE STRING
# PARAMETER OPTIONAL attr6 TYPE STRING
# PARAMETER OPTIONAL attr7 TYPE STRING
# RUNTIME python3

import json, os, sys
from itertools import chain, count

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.enforce('kwic.json', '.json')
names.output('triplaux.tsv', names.replace('kwic.json', '-dep.tsv'))

with open('kwic.json', encoding = 'utf-8') as f:
    data = json.load(f)

kwic = data['kwic']

# head = list(kwic[0]['tokens'][0]) # lead token
# should make some relational sanity checks here
head = tuple(filter(None, (attr0, attr1, attr2, attr3,
                           attr4, attr5, attr6, attr7)))

# also: kMsen (counter), kMtok (counter within kMsen)
# not sure if there should be kMmatch or bMmatch or some such some day (Boolean?)
# the new naming scheme with these prefixen indicates types to ODS-maker and such

# Fragile! This code trusts the annotation to be such that each token
# is a token and has a "ref" and a "dephead" whose value is a "ref"
# except when "0" and there is also a "deprel" - this might not always
# be the case.

with open('triplaux.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('kMsen', 'kMtok',
          *chain(map('{}1'.format, head),
                 ['deprel'],
                 map('{}2'.format, head)),
          sep = '\t',
          file = out)
    for j, hit in enumerate(kwic):
        rex = { tok['ref'] : tok
                for tok in hit['tokens']
                if 'ref' in tok } # is this wise?
        for k, dep in enumerate(hit['tokens']):
            if dep['dephead'] == '0': continue
            # m = hit['match'] # int(m['start'] <= k < m['end']),
            hed = rex[dep['dephead']]
            print(j, k,
                  *chain((dep[key] for key in head),
                         [dep['deprel']],
                         (hed[key] for key in head)),
                  sep = '\t',
                  file = out)
        
os.rename('triplaux.tmp', 'triplaux.tsv')

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
