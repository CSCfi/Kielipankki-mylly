# TOOL korp-kwic-vks.py: "VKS concordance"
# (Search VKS corpus in korp.csc.fi for a KWIC concordance. Query file contains CQP expression that must match. The last expression defines Key Word. Concordance is saved in Korp JSON format.)
# INPUT query.cqp.txt: "Query file" TYPE GENERIC
#     (One or more CQP expressions)
# OUTPUT result.json
# PARAMETER corpus TYPE [
#   VKS_AGRICOLA: "VKS_AGRICOLA",
#   VKS_ALMANAKAT: "VKS_ALMANAKAT",
#   VKS_BIBLIA: "VKS_BIBLIA",
#   VKS_BJORKQVIST: "VKS_BJORKQVIST",
#   VKS_FROSTERUS: "VKS_FROSTERUS",
#   VKS_GANANDER: "VKS_GANANDER",
#   VKS_LAIT: "VKS_LAIT",
#   VKS_LIZELIUS: "VKS_LIZELIUS",
#   VKS_LPETRI: "VKS_LPETRI",
#   VKS_SAARNAT: "VKS_SAARNAT",
#   VKS_VARIA: "VKS_VARIA",
#   VKS_VIRRET: "VKS_VIRRET"
# ] DEFAULT VKS_AGRICOLA
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999
#     (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0
#     (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)
# IMAGE comp-16.04-mylly
# RUNTIME python3

# This tool specifies attributes for a particular corpus.
# NB. 10/12 corpora have text_year, 2/12 have text_author

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

    word word_completed word_tilde

'''.split())

META = comma.join('''

    div_n sentence_code sentence_cRef sentence_id sentence_type
    span_page supplement_cRef text_datefrom text_dateto
    text_distributor_en text_distributor_fi text_filename
    text_timefrom text_timeto text_title text_year

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
