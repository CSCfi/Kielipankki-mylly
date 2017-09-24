# TOOL korp-kwic-ylilauta.py: "Get Korp KWIC concordance from Ylilauta corpus"
# (Queries korp.csc.fi for a KWIC concordance from Ylilauta corpus. Input file contains CQP expressions separated by empty lines. They must all match. The last of them defines the final match. Output file is the concordance in the Korp JSON form.)
# INPUT query.cqp.txt TYPE GENERIC
# OUTPUT result.korp.json
# PARAMETER corpus TYPE [
#     YLILAUTA: "YLILAUTA"
# ] DEFAULT YLILAUTA
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999 (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0 (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)
# RUNTIME python3

# This tool specifies attributes for a particular corpus.

import json, math, random

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_korp import parse_queries, request_kwic
import lib_names as names

# enforce *something* sensible because it seems all too easy to use a
# multimegabyte concordance file (*.json) as a "query" in Mylly GUI;
# query parser in lib_korp also tries to guard against nonsense in
# content by now
names.enforce('query.cqp.txt', '.cqp.txt')

seed = random.randrange(1000, 10000) if math.isnan(seed) else seed
names.output('result.korp.json',
             names.replace('query.cqp.txt',
                           '-s{}p{}.korp.json'.format(seed, page)))

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

QUERIES = parse_queries('query.cqp.txt')

kwic = request_kwic(corpus = CORPUS,
                    seed = seed,
                    size = 1000,
                    page = page,
                    anno = ANNO,
                    meta = META,
                    queries = QUERIES)

# note: it *adds* dict(M = dict(origin = size * page)) to the kwic

with open('result.korp.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(kwic, result,
              ensure_ascii = False,
              check_circular = False)
