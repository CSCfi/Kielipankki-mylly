# TOOL suomi24-kwic.py: "Korp KWIC Suomi24"
# (Query Korp for a concordance from Suomi24 corpus.
# Input file contains CQP expressions, separated by an empty line,
# that must all match, and the last expression defines the final
# match region. Output file is the concordance in a JSON form.)
# INPUT cqps.txt TYPE GENERIC
# OUTPUT conc.json
# RUNTIME python3

from itertools import count, groupby
import json
import requests

import lib_names as names
names.output('conc.json', names.replace('cqps.txt', '.json'))

KORP = 'https://korp.csc.fi/cgi-bin/korp.cgi'

# Make this be for Suomi24, and another tool for another set of
# corpora. Corpus selection is not a parameter at all. The queries are
# in an input file. The tool can know what attributes are appropriate
# to its corpus.

with open('cqps.txt') as cqps:
    ooKEY = ( ('cqp{}'.format(k) if k else 'cqp') for k in count() )
    ooCQP = ( ' '.join(lines).strip()
              for between, lines in groupby(cqps, str.isspace)
              if not between )
    QUERYZ = dict(zip(ooKEY, ooCQP))

CORPUS = 'S24'
ANNO = 'lemma,pos,msd,dephead,reprel,ref,lex,nertag'
META = 'sentence_id,text_title,text_date,text_time,text_sect,text_sub,text_user,sentence_id,text_urlmsg,text_urlboard'

# https://www.kielipankki.fi/support/korpapi/

it = dict(command='query',
          corpus = CORPUS,
          sort = 'random',
          # random_seed = '1278',
          defaultcontext='1 sentence',
          defaultwithin='sentence',
          start='0',
          end='999',
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

r = requests.get(KORP, params = it, timeout = 10.0)
r.raise_for_status()

# response can be an error message in JSON, or a concordance;
# to detect error message, so only a concordance goes to file

with open('conc.json', mode = 'w', encoding = 'utf-8') as conc:
    json.dump(r.json(), conc,
              ensure_ascii = False,
              check_circular = False)
