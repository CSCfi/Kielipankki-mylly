# TOOL cqp-two.py: "Simple two-token query"
# (Make a CQP query to match one or two given values of one or two tokens. The query can be used to find matches in sentences.)
# OUTPUT query.cqp
# PARAMETER qbase: "Query file base name" TYPE STRING DEFAULT "two"
# PARAMETER key1a: "First attribute of first token" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     deprel: deprel
# ] DEFAULT word (An attribute of a token)
# PARAMETER val1a: "Value" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER key1b: "Second attribute" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     deprel: deprel
# ] DEFAULT word (Another attribute of the same token)
# PARAMETER OPTIONAL val1b: "Value" TYPE STRING
#     (A value of the attribute)
# PARAMETER key2a: "First attribute of second token" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     deprel: deprel
# ] DEFAULT word (An attribute of a second token)
# PARAMETER OPTIONAL val2a: "Value" TYPE STRING
#     (A value of the attribute)
# PARAMETER key2b: "Second attribute" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     deprel: deprel
# ] DEFAULT word (Another attribute of the second token)
# PARAMETER OPTIONAL val2b: "Value" TYPE STRING
#    (A value of the attribute)
# RUNTIME python3

from itertools import chain
import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import name
name('query.cqp', qbase, ext = 'cqp.txt')

if not all((c.isalpha() or c.isdigit() or c in '-,.')
           for c in chain(filter(None, (val1a, val1b,
                                        val2a, val2b)))):
    print('Only letters, digits, hyphen, comma, and period allowed;',
          'or this may be a locale problem on the server,',
          'maybe one cannot even say "hyvää päivää",', # testing!
          'which surely is a cause for mortification:',
          *map(repr, (val1a, val1b, val2a, val2b)),
          sep = '\n',
          file = sys.stderr)
    exit(1)

with open('query.tmp', mode = 'w', encoding = 'utf-8') as out:
    # who writes code like this
    print('[',
          ' &\n  '.join('{} = "{}"'.format(key, val)
                        for key, val in ((key1a, val1a),
                                         (key1b, val1b))
                        if val),
          ']',
          file = out)
    
    if val2a or val2b:
        print(file = out)
        print('[',
              ' &\n  '.join('{} = "{}"'.format(key, val)
                            for key, val in ((key2a, val2a),
                                             (key2b, val2b))
                            if val),
              ']',
              file = out)

os.rename('query.tmp', 'query.cqp')
