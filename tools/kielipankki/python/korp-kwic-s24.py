# TOOL korp-kwic-s24.py: "Suomi24 concordance"
# (Search Suomi24 corpus korp.csc.fi for a KWIC concordance. Query file contains CQP expressions that must match. The last expression defines Key Word. Concordance is saved in Korp JSON format.)
# INPUT query.cqp: "Query file" TYPE GENERIC
#     (One or more CQP expressions)
# OUTPUT result.json
# PARAMETER corpus: "Corpus" TYPE [
#     S24: "S24",
#     S24_001: "S24_001",
#     S24_002: "S24_002",
#     S24_003: "S24_003",
#     S24_004: "S24_004",
#     S24_005: "S24_005",
#     S24_006: "S24_006",
#     S24_007: "S24_007",
#     S24_008: "S24_008",
#     S24_009: "S24_009",
#     S24_010: "S24_010"
# ] DEFAULT S24_001
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999
#     (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0
#     (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)

# This tool specifies attributes for a particular corpus.

# NB. Amazingly, subcorpus keys in header have been broken until now.

# NB. Including only attributes as are in at least 11 subcorpora.
# NB. This still means that some of them are missing in one!
# NB. Does the one then crash? Or does it produce incompatible output?
# NB. Removed S24_011: "S24_011" - is a piece that failed to parse?

import json, math, random

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_korp import parse_queries, request_kwic
from lib_names2 import base, name

seed = random.randrange(1000, 10000) if math.isnan(seed) else seed

name('result.json', base('query.cqp', '*.cqp.txt'),
     ins = 'kwic-{}-s{}-p{}'.format(corpus, seed, page),
     ext = 'korp.json')

comma = ','

CORPUS = corpus # 'S24'

ANNO = comma.join('''

    lemma lemmacomp word pos msd dephead deprel ref lex nertag nerbio

'''.split())

# omitting ne attributes as they are presumably subsentence attributes
META = comma.join('''

        paragraph_id sentence_id text_anonnick text_anonnick_lemmas
        text_cid text_comms text_date text_datefrom text_dateto
        text_discussionarea text_sect text_ssssssubsect
        text_sssssubsect text_ssssubsect text_sssubsect text_ssubsect
        text_subsect text_subsections text_tid text_time text_timefrom
        text_timeto text_title text_title_lemmas text_urlboard
        text_urlmsg text_views text_year

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
