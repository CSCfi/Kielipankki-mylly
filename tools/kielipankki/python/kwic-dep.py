# TOOL kwic-dep.py: "KWIC dependency triples as relation"
# (Write dependents and their heads, together with the type of dependency, from a dependency-annotated Korp JSON-form concordance, as a TSV relation file. One or more positional attributes are suffixed with 1 for the dependent and 2 for the head. Sentence and token counters, kMsen and kMtok, identify each occurrence.)
# INPUT kwic.json: "Concordance file" TYPE GENERIC
#     (A KWIC concordance in a Korp JSON file)
# OUTPUT triplaux.tsv
# PARAMETER attr0: "Attribute" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     msd: msd
# ] (An attribute to include for dependent and head in a triple)
# PARAMETER OPTIONAL attr1: "Attribute" TYPE [
#     word: word,
#     lemma, lemma,
#     pos: pos,
#     msd: msd
# ]
# PARAMETER OPTIONAL attr2: "Attribute" TYPE [
#     word: word,
#     lemma, lemma,
#     pos: pos,
#     msd: msd
# ]
# PARAMETER OPTIONAL attr3: "Attribute" TYPE [
#     word: word,
#     lemma, lemma,
#     pos: pos,
#     msd: msd
# ]
# PARAMETER OPTIONAL attr4: "Attribute" TYPE STRING
# PARAMETER OPTIONAL attr5: "Attribute" TYPE STRING
# PARAMETER OPTIONAL attr6: "Attribute" TYPE STRING
# PARAMETER OPTIONAL attr7: "Attribute" TYPE STRING
# IMAGE comp-16.04-mylly
# RUNTIME python3

import json, os, sys
from itertools import chain, count

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name("triplaux.tsv", base('kwic.json', '*.korp.json'),
     ins = 'dep',
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
