# TOOL simple-cqp.py: "Prepare simple query"
# (Prepare simple CQP query to match sentences that satisfy one or two conditions, each condition describing a single token in a limited way.)
# OUTPUT query.txt
# PARAMETER key1a: "Attribute of  a token" TYPE [word: word, lemma: lemma, pos: pos, deprel: deprel] DEFAULT word (An attribute of a token)
# PARAMETER val1a: "Value of the attribute" TYPE STRING (Value of the attribute for the token (letters, digits, hyphen, comma, period\))
# PARAMETER key1b: "Attribute of the token" TYPE [word: word, lemma: lemma, pos: pos, deprel: deprel] DEFAULT word (Another attribute of the token)
# PARAMETER OPTIONAL val1b: "Value of the attribute" TYPE STRING (Value of the attribute)
# PARAMETER key2a: "Attribute of  a token" TYPE [word: word, lemma: lemma, pos: pos, deprel: deprel] DEFAULT word (An attribute of a token)
# PARAMETER OPTIONAL val2a: "Value of the attribute" TYPE STRING (Value of the attribute for the token (letters, digits, hyphen, comma, period\))
# PARAMETER key2b: "Attribute of the token" TYPE [word: word, lemma: lemma, pos: pos, deprel: deprel] DEFAULT word (Another attribute of the token)
# PARAMETER OPTIONAL val1b: "Value of the attribute" TYPE STRING (Value of the attribute)

from itertools import chain
import os, sys

if not all((c.isalpha() or c.isdigit() or c in '-,.')
           for c in chain(filter(None, (val1a, val1b,
                                        val2a, val2b)))):
    print('Only letters, digits, hyphen, comma, and period allowed',
          file = sys.stderr)
    exit(1)

with open('query.tmp', mode = 'w', encoding = 'utf-8') as out:
    print('[ {} = "{}" ]'.format(key1a, val1a), file = out)
    if val1b: print('[ {} = "{}" ]'.format(key1b, val1b), file = out)
    if val2a or val2b: print(file = out)
    if val2a: print('[ {} = "{}" ]'.format(key2a, val2a), file = out)
    if val2b: print('[ {} = "{}" ]'.format(key2b, val2b), file = out)

os.rename('query.tmp', 'query.txt')
