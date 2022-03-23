# TOOL cqp-alt.py: "Simple alternatives query"
# (Make a CQP query to match any of the given values for a specified attribute. The query can be used to find matches in sentences.)
# OUTPUT query.cqp
# PARAMETER qbase: "Query file base name" TYPE STRING DEFAULT "alt"
# PARAMETER key: "An attribute" TYPE [
#     word: word,
#     lemma: lemma,
#     pos: pos,
#     deprel: deprel
# ] DEFAULT word (An attribute of a token)
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

from itertools import chain
import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import name
name('query.cqp', qbase, ext = 'cqp.txt')

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
    
os.rename('query.tmp', 'query.cqp')
