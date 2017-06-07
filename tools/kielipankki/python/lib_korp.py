from itertools import count, groupby
import json
import requests

KORP = 'https://korp.csc.fi/cgi-bin/korp.cgi'

def parse_queries(filename):
    '''Dict of line-separated queries from the file, keyed with cqp, cqp1, ...'''
    with open(filename) as query:
        ooKEY = ( ('cqp{}'.format(k) if k else 'cqp') for k in count() )
        ooCQP = ( ' '.join(lines).strip()
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

    Halt execution on error response or empty concordance. The latter
    is because in an empty concordance positional attributes are not
    named, and the result can then not be transformed into a tabular
    form that is compatible with non-empty tables from the same
    source.

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

    response = requests.get(KORP, params = it, timeout = 30.0)
    response.raise_for_status()

    result = response.json()

    if 'ERROR' in result:
        print(result['ERROR']['type'],
              result['ERROR']['message'],
              file = sys.stderr)
        exit(1)

    if result['hits'] == 0:
        print('empty concordance (no positional names)',
              file = sys.stderr)
        exit(1)

    if 'M' in result:
        print('cannot extend result, it already has "M" - please report',
              file = sys.stderr)
        exit(1)

    # record starting point so that the TSV algebra can safely combine
    # different pages from the same source - could record other things
    result['M'] = dict(origin = size * page)

    return result
