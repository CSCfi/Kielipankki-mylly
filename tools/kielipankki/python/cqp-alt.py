# TOOL cqp-alt.py: "Make CQP query for a single-token set of values"
# (Make CQP to that matches a token with any of the given values for the specified attribute.)
# OUTPUT query.cqp.txt
# PARAMETER key: "An attribute" TYPE [word: word, lemma: lemma, pos: pos, deprel: deprel] DEFAULT word
#     (An attribute of a token)
# PARAMETER val0: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER OPTIONAL val1: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER OPTIONAL val2: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER OPTIONAL val3: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER OPTIONAL val4: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER OPTIONAL val5: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER OPTIONAL val6: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER OPTIONAL val7: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER OPTIONAL val8: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# PARAMETER OPTIONAL val9: "A value of the attribute" TYPE STRING
#     (A value of the attribute (letters, digits, hyphen, comma, period\))
# RUNTIME python3

from itertools import chain
import os, sys

if not all((c.isalpha() or c.isdigit() or c in '-,.')
           for c in chain(filter(None, (val0, val1, val2, val3, val4,
                                        val5, val6, val7, val8, val9)))):
    print('Only letters, digits, hyphen, comma, and period allowed',
          file = sys.stderr)
    exit(1)

with open('query.tmp', mode = 'w', encoding = 'utf-8') as out:
    # who writes code like this
    print('[',
          ' |\n  '.join('{} = "{}"'.format(key, val)
                        for val in (val0, val1, val2, val3, val4,
                                    val5, val6, val7, val8, val9)
                        if val),
          ']',
          file = out)
    
os.rename('query.tmp', 'query.cqp.txt')
