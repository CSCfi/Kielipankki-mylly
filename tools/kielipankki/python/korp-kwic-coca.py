# TOOL korp-kwic-coca.py: "Get Korp KWIC concordance from COCA corpus"
# (Queries korp.csc.fi for a KWIC concordance from COCA corpus. Input file contains CQP expressions separated by empty lines. They must all match. The last of them defines the final match. Output file is the concordance in the Korp JSON form.)
# INPUT query.cqp TYPE GENERIC
# OUTPUT result.json
# PARAMETER corpus TYPE [
#     COCA_ACAD: "COCA_ACAD",
#     COCA_FIC: "COCA_FIC",
#     COCA_MAG: "COCA_MAG",
#     COCA_NEWS: "COCA_NEWS",
#     COCA_SPOK: "COCA_SPOK"
# ] DEFAULT COCA_ACAD
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999 (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0 (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)
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

ANNO = comma.join('lemma lex pos posorig word'.split())

META = comma.join('''

      paragraph_id paragraph_type sentence_gaps sentence_id
      text_datefrom text_dateto text_filename text_genre text_id
      text_publ_info text_source text_subgenre text_timefrom
      text_timeto text_title text_wordcount text_year

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
