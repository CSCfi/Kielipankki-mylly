# TOOL korp-kwic-coha.py: "Get Korp KWIC concordance from COHA corpus"
# (Queries korp.csc.fi for a KWIC concordance from COHA corpus. Input file contains CQP expressions separated by empty lines. They must all match. The last of them defines the final match. Output file is the concordance in the Korp JSON form.)
# INPUT query.cqp TYPE GENERIC
# OUTPUT result.json
# PARAMETER corpus TYPE [
#      COHA_1810S_FIC: "COHA_1810S_FIC",
#      COHA_1810S_MAG: "COHA_1810S_MAG",
#      COHA_1810S_NF: "COHA_1810S_NF",
#      COHA_1820S_FIC: "COHA_1820S_FIC",
#      COHA_1820S_MAG: "COHA_1820S_MAG",
#      COHA_1820S_NF: "COHA_1820S_NF",
#      COHA_1830S_FIC: "COHA_1830S_FIC",
#      COHA_1830S_MAG: "COHA_1830S_MAG",
#      COHA_1830S_NF: "COHA_1830S_NF",
#      COHA_1840S_FIC: "COHA_1840S_FIC",
#      COHA_1840S_MAG: "COHA_1840S_MAG",
#      COHA_1840S_NF: "COHA_1840S_NF",
#      COHA_1850S_FIC: "COHA_1850S_FIC",
#      COHA_1850S_MAG: "COHA_1850S_MAG",
#      COHA_1850S_NF: "COHA_1850S_NF",
#      COHA_1860S_FIC: "COHA_1860S_FIC",
#      COHA_1860S_MAG: "COHA_1860S_MAG",
#      COHA_1860S_NEWS: "COHA_1860S_NEWS",
#      COHA_1860S_NF: "COHA_1860S_NF",
#      COHA_1870S_FIC: "COHA_1870S_FIC",
#      COHA_1870S_MAG: "COHA_1870S_MAG",
#      COHA_1870S_NEWS: "COHA_1870S_NEWS",
#      COHA_1870S_NF: "COHA_1870S_NF",
#      COHA_1880S_FIC: "COHA_1880S_FIC",
#      COHA_1880S_MAG: "COHA_1880S_MAG",
#      COHA_1880S_NEWS: "COHA_1880S_NEWS",
#      COHA_1880S_NF: "COHA_1880S_NF",
#      COHA_1890S_FIC: "COHA_1890S_FIC",
#      COHA_1890S_MAG: "COHA_1890S_MAG",
#      COHA_1890S_NEWS: "COHA_1890S_NEWS",
#      COHA_1890S_NF: "COHA_1890S_NF",
#      COHA_1900S_FIC: "COHA_1900S_FIC",
#      COHA_1900S_MAG: "COHA_1900S_MAG",
#      COHA_1900S_NEWS: "COHA_1900S_NEWS",
#      COHA_1900S_NF: "COHA_1900S_NF",
#      COHA_1910S_FIC: "COHA_1910S_FIC",
#      COHA_1910S_MAG: "COHA_1910S_MAG",
#      COHA_1910S_NEWS: "COHA_1910S_NEWS",
#      COHA_1910S_NF: "COHA_1910S_NF",
#      COHA_1920S_FIC: "COHA_1920S_FIC",
#      COHA_1920S_MAG: "COHA_1920S_MAG",
#      COHA_1920S_NEWS: "COHA_1920S_NEWS",
#      COHA_1920S_NF: "COHA_1920S_NF",
#      COHA_1930S_FIC: "COHA_1930S_FIC",
#      COHA_1930S_MAG: "COHA_1930S_MAG",
#      COHA_1930S_NEWS: "COHA_1930S_NEWS",
#      COHA_1930S_NF: "COHA_1930S_NF",
#      COHA_1940S_FIC: "COHA_1940S_FIC",
#      COHA_1940S_MAG: "COHA_1940S_MAG",
#      COHA_1940S_NEWS: "COHA_1940S_NEWS",
#      COHA_1940S_NF: "COHA_1940S_NF",
#      COHA_1950S_FIC: "COHA_1950S_FIC",
#      COHA_1950S_MAG: "COHA_1950S_MAG",
#      COHA_1950S_NEWS: "COHA_1950S_NEWS",
#      COHA_1950S_NF: "COHA_1950S_NF",
#      COHA_1960S_FIC: "COHA_1960S_FIC",
#      COHA_1960S_MAG: "COHA_1960S_MAG",
#      COHA_1960S_NEWS: "COHA_1960S_NEWS",
#      COHA_1960S_NF: "COHA_1960S_NF",
#      COHA_1970S_FIC: "COHA_1970S_FIC",
#      COHA_1970S_MAG: "COHA_1970S_MAG",
#      COHA_1970S_NEWS: "COHA_1970S_NEWS",
#      COHA_1970S_NF: "COHA_1970S_NF",
#      COHA_1980S_FIC: "COHA_1980S_FIC",
#      COHA_1980S_MAG: "COHA_1980S_MAG",
#      COHA_1980S_NEWS: "COHA_1980S_NEWS",
#      COHA_1980S_NF: "COHA_1980S_NF",
#      COHA_1990S_FIC: "COHA_1990S_FIC",
#      COHA_1990S_MAG: "COHA_1990S_MAG",
#      COHA_1990S_NEWS: "COHA_1990S_NEWS",
#      COHA_1990S_NF: "COHA_1990S_NF",
#      COHA_2000S_FIC: "COHA_2000S_FIC",
#      COHA_2000S_MAG: "COHA_2000S_MAG",
#      COHA_2000S_NEWS: "COHA_2000S_NEWS",
#      COHA_2000S_NF: "COHA_2000S_NF"
# ] DEFAULT COHA_1810S_FIC
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

CORPUS = corpus # 'S24'

ANNO = comma.join('lemma lex pos posorig word'.split())

META = comma.join('''

      paragraph_id paragraph_type sentence_gaps sentence_id
      text_author text_datefrom text_dateto text_filename text_fixed
      text_genre text_id text_lcc text_publ_info text_timefrom
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
