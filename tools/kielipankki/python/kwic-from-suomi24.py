# TOOL kwic-from-suomi24.py: "Concordance from Suomi24 corpus in Korp"
# (Queries Korp for a KWIC concordance from Suomi24 corpus. Input file contains CQP expressions, separated by empty lines, that must all match, and the last expression defines the final match region. Output file is the concordance in a JSON form.)
# INPUT query.txt TYPE GENERIC
# OUTPUT result.json
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999 (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0 (Extract the specified page 0-9, of 1000 results each, from the concordance.)
# RUNTIME python3

from itertools import count, groupby
from math import isnan
import json, random
import requests

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

seed = random.randrange(1000, 10000) if isnan(seed) else seed
names.output('result.json', names.replace('query.txt', '-s{}-p{}.json'.format(seed, page)))

KORP = 'https://korp.csc.fi/cgi-bin/korp.cgi'

# Make this be for Suomi24, and another tool for another set of
# corpora. Corpus selection is not a parameter at all. The queries are
# in an input file. The tool can know what attributes are appropriate
# to its corpus.

with open('query.txt') as query:
    ooKEY = ( ('cqp{}'.format(k) if k else 'cqp') for k in count() )
    ooCQP = ( ' '.join(lines).strip()
              for between, lines in groupby(query, str.isspace)
              if not between )
    QUERYZ = dict(zip(ooKEY, ooCQP))

CORPUS = 'S24'
ANNO = 'lemma,pos,msd,dephead,deprel,ref,lex,nertag'
META = 'sentence_id,text_title,text_date,text_time,text_sect,text_sub,text_user,sentence_id,text_urlmsg,text_urlboard'

# https://www.kielipankki.fi/support/korpapi/

it = dict(command = 'query',
          corpus = CORPUS,
          sort = 'random',
          random_seed = seed,
          defaultcontext = '1 sentence',
          defaultwithin = 'sentence',
          start = page * 1000,
          end = (page + 1) * 1000 - 1,
          show = ANNO,
          show_struct = META)

it.update(QUERYZ)

# Jira this!  looks like (1) show_struct is not optional and (2)
# cannot be empty and (3) the error message for it is "string
# index out of bounds" which is not good -- minimally fix doc [?+]
# --> [+], but it's a bit funny to require that user require
# structural attributes in the result, so a better fix would be to
# make it optional (with or without a default), or at least
# provide an informative error message.

r = requests.get(KORP, params = it, timeout = 30.0)
r.raise_for_status()

it = r.json()

if 'ERROR' in it:
    print(it['ERROR']['type'], it['ERROR']['message'], file = sys.stderr)
    exit(1)

if it['hits'] == 0:
    print('empty concordance (no positional names)', file = sys.stderr)
    exit(1)

with open('result.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(it, result,
              ensure_ascii = False,
              check_circular = False)
