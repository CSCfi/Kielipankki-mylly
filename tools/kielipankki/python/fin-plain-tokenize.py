# TOOL fin-plain-tokenize.py: "Tokenize Finnish plaintext" (Analyze Finnish plaintext into sentences and tokens. Produce both the actual output of the underlying tool and a relation where each sentence and token has an explicit identifier)
# INPUT input.txt TYPE GENERIC
# OUTPUT output.txt
# OUTPUT output.tsv
# RUNTIME python3

# they are not in the proper place yet
DIR = '/wrk/jpiitula/finnish-tagtools'

import os, sys
from itertools import groupby
from subprocess import Popen, PIPE

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
from lib_paths import prepend

name('output.txt', '{}-token'.format(base('input.txt', '*.txt')),
     ext = 'txt')

name('output.tsv', '{}-token'.format(base('input.txt', '*.txt')),
     ext = 'rel.tsv')

# wire to the specific HFST version
VERbin = '/homeappl/appl_taito/ling/hfst/3.13.0/bin'
VERlib = '/homeappl/appl_taito/ling/hfst/3.13.0/lib'
VERENV = dict(os.environ,
              PATH = prepend(VERbin, 'PATH'),
              LD_LIBRARY_PATH = prepend(VERlib, 'LD_LIBRARY_PATH'))

def end(*ps):
    for p in ps:
        try:
            # there should be no more
            # stdout nor stderr there
            p.communicate(timeout = 3)
        except TimeoutExpired as exn:
            # things are already bad
            p.kill()
            p.communicate()
    cs = [p.returncode for p in ps]
    if any((c or (c is None)) for c in cs):
        raise Exception('Non-0 return code in: ' + ' '.join(map(str, cs)))

try:
    with Popen([os.path.join(VERbin, 'hfst-tokenize'),
                os.path.join(DIR, 'tokenize.pmatch')],
               env = VERENV,
               stdin = open('input.txt', mode = 'rb'),
               stdout = PIPE,
               stderr = open('error1.log', mode = 'wb')) as tokenize:
        with Popen(['tee', 'output.txt'],
                   stdin = tokenize.stdout,
                   stdout = PIPE,
                   stderr = open('error2.log', mode = 'wb')) as tee:
            
            # tee saves the actual output in output.txt; then the
            # following writes a corresponding relation in output.tsv
            
            with open('output.tsv', mode = 'w', encoding = 'UTF-8') as out:
                print('sentok', 'kMsen', 'kMtok', 'word',
                      sep = '\t',
                      file = out)
                for k, g in enumerate(( group
                                        for kind, group
                                        in groupby(tee.stdout, bytes.isspace)
                                        if not kind ),
                                      start = 1):
                    for t, w in enumerate(g, start = 1):
                        print('{:04}-{:03}'.format(k, t), k, t, w.decode('UTF-8'),
                              sep = '\t',
                              end = '',
                              file = out)
                # waits with time
                end(tokenize, tee)
except Exception as exn:
    et, ev, tr = sys.exc_info()
    print(ev, file = sys.stderr)
    exit(1)