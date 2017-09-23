# TOOL simple-cqp.py: "Create a simple CQP query file for a Korp KWIC tool"
# (Create a simple CQP query file to match sentences that satisfy one or two conditions. Each condition describes a single token in a limited way.)
# OUTPUT query.cqp.txt
# PARAMETER key1a: "Attribute of  a token" TYPE [word: word, lemma: lemma, pos: pos, deprel: deprel] DEFAULT word (An attribute of a token)
# PARAMETER val1a: "Value of the attribute" TYPE STRING (Value of the attribute for the token (letters, digits, hyphen, comma, period\))
# PARAMETER key1b: "Attribute of the token" TYPE [word: word, lemma: lemma, pos: pos, deprel: deprel] DEFAULT word (Another attribute of the token)
# PARAMETER OPTIONAL val1b: "Value of the attribute" TYPE STRING (Value of the attribute)
# PARAMETER key2a: "Attribute of another token" TYPE [word: word, lemma: lemma, pos: pos, deprel: deprel] DEFAULT word (An attribute of a token)
# PARAMETER OPTIONAL val2a: "Value of the attribute" TYPE STRING (Value of the attribute for the token)
# PARAMETER key2b: "Attribute of the other token" TYPE [word: word, lemma: lemma, pos: pos, deprel: deprel] DEFAULT word (Another attribute of the token)
# PARAMETER OPTIONAL val2b: "Value of the attribute" TYPE STRING (Value of the attribute)
# RUNTIME python3

from itertools import chain
import os, sys

if not all((c.isalpha() or c.isdigit() or c in '-,.')
           for c in chain(filter(None, (val1a, val1b,
                                        val2a, val2b)))):
    print('Only letters, digits, hyphen, comma, and period allowed',
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

os.rename('query.tmp', 'query.cqp.txt')
