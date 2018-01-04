# lib_udpipe.py

import os, sys, traceback
from subprocess import Popen, PIPE
from itertools import groupby
from io import TextIOWrapper

# TO BE INSTALLED IN A PLACE MORE PROPER
BINDIR = '/wrk/jpiitula/udpipe-1.2.0-bin/bin-linux64'
MODELS = '/wrk/jpiitula/udpipe-1.2.0-bin/udpipe-ud-2.0-170801'

def transform(source, out):
    '''Read UD2 data from source, write a corresponding relation out.

    '''
    # using UD names for the UD fields (modulo case)
    # http://universaldependencies.org/format.html
    # kMtok may be a misnomer as these are not tokens as such
    print('kMsentence', 'kMtok',
          'id', 'form', 'lemma',
          'upostag', 'xpostag', 'feats',
          'head', 'deprel', 'deps',
          'misc',
          sep = '\t', file = out)
    
    for sen, sentence in enumerate((group
                                    for space, group
                                    in groupby((line for line in source
                                                if not line.startswith('#')),
                                               key = str.isspace)
                                    if not space),
                                   start = 1):
        for tok, line in enumerate(sentence, start = 1):
            print(sen, tok, line,
                  sep = '\t', end = '',
                  file = out)

def parse_plain(modelfile, inputfile, textfile, relationfile):
    '''Runs udpipe with given model file (in directory MODELS), plain text
    input file, all analysis levels.

    '''
    # should rename error1.log and error2.log
    # but not even sure what to do with them
    try:
        with Popen([os.path.join(BINDIR, 'udpipe'),
                    '--immediate', '--tokenize', '--tag', '--parse',
                    os.path.join(MODELS, modelfile)],
                   stdin = open(inputfile, mode = 'rb'),
                   stdout = PIPE,
                   stderr = open('error1.log', mode = 'wb')) as p:
            with Popen(['tee', textfile],
                       stdin = p.stdout,
                       stdout = PIPE,
                       stderr = open('error2.log', mode = 'wb')) as t:
                with open(relationfile, mode = 'w', encoding = 'UTF-8') as out:
                    transform(TextIOWrapper(t.stdout, encoding = 'UTF-8'), out)

                    # like, when *should* it time out?
                    p.communicate(timeout = 3)
        
        if p.returncode or p.returncode is None:
            raise Exception('Non-0 return code: {}'
                            .format(p.returncode))
    except Exception as exn:
        # traceback.print_exc()
        print(exn, file = sys.stderr)
        exit(1)

def parse_tokens(modelfile, inputfile, textfile, relationfile):
    '''Runs udpipe with given model file (in directory MODELS) on
    tokenized input file, tagging and parsing.

    '''
    # should rename error1.log and error2.log
    # but not even sure what to do with them
    try:
        with Popen([os.path.join(BINDIR, 'udpipe'),
                    '--immediate', '--tag', '--parse',
                    os.path.join(MODELS, modelfile)],
                   stdin = open(inputfile, mode = 'rb'),
                   stdout = PIPE,
                   stderr = open('error1.log', mode = 'wb')) as p:
            with Popen(['tee', textfile],
                       stdin = p.stdout,
                       stdout = PIPE,
                       stderr = open('error2.log', mode = 'wb')) as t:
                with open(relationfile, mode = 'w', encoding = 'UTF-8') as out:
                    transform(TextIOWrapper(t.stdout, encoding = 'UTF-8'), out)

                    # like, when *should* it time out?
                    p.communicate(timeout = 3)
        
        if p.returncode or p.returncode is None:
            raise Exception('Non-0 return code: {}'
                            .format(p.returncode))
    except Exception as exn:
        # traceback.print_exc()
        print(exn, file = sys.stderr)
        exit(1)
