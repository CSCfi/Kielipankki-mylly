# TOOL korp-kwic-ylilauta.py: "Ylilauta concordance"
# (Search Ylilauta corpus in korp.csc.fi for a KWIC concordance. Query file contains CQP expressions that must match. The last expression defines Key Word. Concordance is saved in Korp JSON format.)
# INPUT query.cqp: "Query file" TYPE GENERIC
#     (One or more CQP expressions)
# OUTPUT result.json
# PARAMETER corpus: "Corpus" TYPE [
#     YLILAUTA: "YLILAUTA"
# ] DEFAULT YLILAUTA
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999
#     (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0
#     (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)
# IMAGE comp-16.04-mylly
# RUNTIME python3

# This tool specifies attributes for a particular corpus.

import json, math, random

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_korp import parse_queries, request_kwic
from lib_names2 import base, name

seed = random.randrange(1000, 10000) if math.isnan(seed) else seed

name('result.json', base('query.cqp', '*.cqp.txt'),
     ins = 'kwic-{}-s{}-p{}'.format(corpus, seed, page),
     ext = 'korp.json')

comma = ','

CORPUS = corpus

ANNO = comma.join('''

    word ref lemma lemmacomp pos msd dephead deprel nertag lex

'''.split())

META = comma.join('''

    text_title text_sec text_id text_date text_clock
    text_datefrom text_dateto text_timefrom text_timeto
    paragraph_id sentence_id

'''.split())

QUERIES = parse_queries('query.cqp')

kwic = request_kwic(corpus = CORPUS,
                    seed = seed,
                    size = 1000,
                    page = page,
                    anno = ANNO,
                    meta = META,
                    queries = QUERIES)

# note: it *adds* dict(M = dict(origin = size * page)) to the kwic

with open('result.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(kwic, result,
              ensure_ascii = False,
              check_circular = False)
