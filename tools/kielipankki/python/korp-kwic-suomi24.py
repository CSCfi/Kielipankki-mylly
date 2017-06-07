# TOOL kwic-from-suomi24.py: "Korp KWIC for Suomi24"
# (Queries Korp for a KWIC concordance from Suomi24 corpus. Input file contains CQP expressions, separated by empty lines, that must all match, and the last expression defines the final match region. Output file is the concordance in a JSON form.)
# INPUT query.txt TYPE GENERIC
# OUTPUT result.json
# PARAMETER corpus TYPE [
#     S24: "S24",
#     S24_001: "S24_001",
#     S24_001: "S24_002",
#     S24_001: "S24_003",
#     S24_001: "S24_004",
#     S24_001: "S24_005",
#     S24_001: "S24_006",
#     S24_001: "S24_007",
#     S24_001: "S24_008",
#     S24_001: "S24_009",
#     S24_001: "S24_009TEST",
#     S24_001: "S24_010",
#     S24_001: "S24_011"
# ] DEFAULT S24
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999 (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0 (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)
# RUNTIME python3

# This tool specifies attributes for a particular corpus.

import json, math, random

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_korp import parse_queries, request_kwic
import lib_names as names

seed = random.randrange(1000, 10000) if math.isnan(seed) else seed
names.output('result.json', names.replace('query.txt', '-s{}p{}.json'.format(seed, page)))

comma = ','

CORPUS = corpus # 'S24'

ANNO = comma.join('lemma pos msd dephead deprel ref lex nertag'.split())

META = comma.join('''

    sentence_id
    text_title  text_date  text_time
    text_sect  text_sub  text_user
    text_urlmsg  text_urlboard

    '''.split())

QUERIES = parse_queries('query.txt')

kwic = request_kwic(corpus = CORPUS,
                    seed = seed,
                    size = 1000,
                    page = page,
                    anno = ANNO,
                    meta = META,
                    queries = QUERIES)

with open('result.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(kwic, result,
              ensure_ascii = False,
              check_circular = False)
