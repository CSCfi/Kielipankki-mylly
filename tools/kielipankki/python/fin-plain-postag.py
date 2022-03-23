# TOOL fin-plain-postag.py: "Classify words in Finnish plaintext" (PoS-tag Finnish plaintext. Produce both the actual output of the underlying tool and a relation where each sentence and token has an explicit identifier.)
# INPUT input.txt TYPE GENERIC
# OUTPUT output.txt
# OUTPUT output.tsv

import os, sys
from itertools import groupby
from subprocess import Popen, PIPE

sys.path.append(os.path.join(chipster_module_path, "python"))
sys.path.append(os.path.join(chipster_module_path, "python/xvrt-tools"))
from lib_names2 import base, name

# temporary copy of outsidelib from vrt-tools, primarily to access a
# workable locale, secondarily to use more convenient path machinery
from outsidelib import prebins, prelibs, HFSTBIN, HFSTLIB, utf8ish
from outsidelib import FINPOS

name('output.txt', '{}-pos'.format(base('input.txt', '*.txt')),
     ext = 'txt')

name('output.tsv', '{}-pos'.format(base('input.txt', '*.txt')),
     ext = 'rel.tsv')

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
    with Popen([FINPOS],
               # finnish-postag needs HFST bin and lib (for
               # hfst-tokenize, hfst-lookup) on respective paths, and
               # a locale that does UTF-8 (for its Python scripts),
               # none of which Mylly has (2019-04-18)
               env = dict(os.environ,
                          LC_ALL = utf8ish(),
                          PATH = prebins(HFSTBIN),
                          LD_LIBRARY_PATH = prelibs(HFSTLIB)),
               stdin = open('input.txt', mode = 'rb'),
               stdout = PIPE) as tokenize:

        with Popen(['tee', 'output.txt'],
                   stdin = tokenize.stdout,
                   stdout = PIPE) as tee:
            
            # tee saves the actual output in output.txt; then the
            # following writes a corresponding relation in output.tsv
            
            with open('output.tsv', mode = 'w', encoding = 'UTF-8') as out:
                print('sentok', 'kMsen', 'kMtok', 'word', 'lemma', 'msd',
                      sep = '\t',
                      file = out)
                for k, g in enumerate(( group
                                        for kind, group
                                        in groupby(tee.stdout, bytes.isspace)
                                        if not kind ),
                                      start = 1):
                    for t, wbm in enumerate(g, start = 1):
                        w, b, m = wbm.decode('UTF-8').split('\t')
                        m = m.strip('[]\r\n').replace(']|[', '|') or '_'
                        print('{:04}-{:03}'.format(k, t), k, t, w, b, m,
                              sep = '\t',
                              file = out)
                # waits with time
                end(tokenize, tee)
except Exception as exn:
    et, ev, tr = sys.exc_info()
    print(ev, file = sys.stderr)
    exit(1)
