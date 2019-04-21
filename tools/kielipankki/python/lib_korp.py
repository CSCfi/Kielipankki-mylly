from itertools import count, groupby
import json, os, sys
import requests

KORP = 'https://korp.csc.fi/cgi-bin/korp.cgi'

def look_like_query(line):
    '''Identity if line looks even minimally like a CQP expression, else
    go down in flames (though with a friendly message, of course).

    This is to protect a Mylly user when they accidentally use a
    completely wrong file as their query. Used in parse_queries below.

    '''

    if line.startswith('[') and line.endswith(']'):
        return line

    print('Query looks suspiciously unexpected', file = sys.stderr)
    exit(1)

def parse_queries(filename):

    '''Dict of line-separated queries from the file, keyed with cqp, cqp1, ...'''

    if os.path.getsize(filename) > 1999: # bytes
        print('Query file looks suspiciously long', file = sys.stderr)
        exit(1)

    with open(filename) as query:
        ooKEY = ( ('cqp{}'.format(k) if k else 'cqp') for k in count() )
        ooCQP = ( look_like_query(' '.join(lines).strip())
                  for between, lines in groupby(query, str.isspace)
                  if not between )
        return dict(zip(ooKEY, ooCQP))


def request_kwic(*,
                 corpus,
                 seed,
                 size = 1000,
                 page,
                 anno,
                 meta,
                 queries):

    '''Query KORP for a KWIC, see
    https://www.kielipankki.fi/support/korpapi/.

    Return the KWIC as a dict.

    Halt execution on timeout or an error response or an empty
    concordance. The latter is because in an empty concordance
    positional attributes are not named, and the result can then not
    be transformed into a tabular form that is compatible with
    non-empty tables from the same source.

    '''

    it = dict(command = 'query',
              corpus = corpus,
              sort = 'random',
              random_seed = seed,
              defaultcontext = '1 sentence',
              defaultwithin = 'sentence',
              start = page * size,
              end = (page + 1) * size - 1,
              show = anno,
              show_struct = meta)
    
    it.update(queries)

    try:
        response = requests.get(KORP, params = it, timeout = 180.0)
        response.raise_for_status()
    except Exception as exn:
        print(type(exn), exn, file = sys.stderr)
        exit(1)

    result = response.json()

    if 'ERROR' in result:
        print(result['ERROR']['type'],
              result['ERROR']['value'],
              file = sys.stderr)
        exit(1)

    if len(result['kwic']) == 0:
        print('empty concordance (no positional names)',
              file = sys.stderr)
        exit(1)

    if 'M' in result:
        # untested code
        print('cannot extend result, result already has "M" - please report',
              file = sys.stderr)
        exit(1)

    # record starting point so that the TSV algebra can safely combine
    # different pages from the same source - could record other things
    result['M'] = dict(origin = size * page)

    return result

def request_info(*, corpora):

    '''Query KORP for INFO on corpora, see
    https://www.kielipankki.fi/support/korpapi/.

    Return the INFO as a dict.

    Halt execution on timeout or an error response.

    '''

    it = dict(command = 'info',
              corpus = corpora)

    try:
        response = requests.get(KORP, params = it, timeout = 180.0)
        response.raise_for_status()
    except Exception as exn:
        print(type(exn), exn, file = sys.stderr)
        exit(1)

    result = response.json()

    if 'ERROR' in result:
        print(result['ERROR']['type'],
              result['ERROR']['message'],
              file = sys.stderr)
        exit(1)

    return result

def request_list():

    ''' '''

    it = dict(command = 'info')

    try:
        response = requests.get(KORP, params = it, timeout = 180.0)
        response.raise_for_status()
    except Exception as exn:
        print(type(exn), exn, file = sys.stderr)
        exit(1)

    result = response.json()

    if 'ERROR' in result:
        print(result['ERROR']['type'],
              result['ERROR']['message'],
              file = sys.stderr)
        exit(1)

    return result
