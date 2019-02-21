# TOOL korp-kwic-s24.py: "Get Korp KWIC concordance from Suomi24 corpus"
# (Queries korp.csc.fi for a KWIC concordance from Suomi24 corpus. Input file contains CQP expressions separated by empty lines. They must all match. The last of them defines the final match. Output file is the concordance in the Korp JSON form.)
# INPUT query.cqp.txt TYPE GENERIC
# OUTPUT result.korp.json
# PARAMETER corpus TYPE [
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
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999 (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0 (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)
# RUNTIME python3

# This tool specifies attributes for a particular corpus.

# NB. Amazingly, subcorpus keys in header have been broken until now.

# NB. Including only attributes as are in at least 11 subcorpora.
# NB. This still means that some of them are missing in one!
# NB. Does the one then crash? Or does it produce incompatible output?
# NB. Removed S24_011: "S24_011" - is a piece that failed to parse?

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

QUERIES = parse_queries('query.cqp.txt')

try:
    kwic = request_kwic(corpus = CORPUS,
                        seed = seed,
                        size = 1000,
                        page = page,
                        anno = ANNO,
                        meta = META,
                        queries = QUERIES)
except Exception as exn:
    # attempt to give a nicer message
    # (should really catch exact type, but need to work out what it is)
    print('Exception:', exn, file = sys.stderr)
    print('Exception type:', type(exn), file = sys.stderr)
    print('The Korp server did not respond in time.',
          'A second or third attempt may succeed',
          sep = '\n',
          file = sys.stderr)

# note: it *adds* dict(M = dict(origin = size * page)) to the kwic

with open('result.korp.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(kwic, result,
              ensure_ascii = False,
              check_circular = False)
