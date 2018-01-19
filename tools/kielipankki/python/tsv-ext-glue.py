# TOOL tsv-ext-glue.py: "Glue attributes" (Extend relation with selected attributes glued into a new attribute.)
# INPUT input.tsv TYPE GENERIC
# OUTPUT output.tsv
# PARAMETER newattr: "New attribute" TYPE STRING
# PARAMETER glue TYPE [space, colon, hyphen, slash] DEFAULT space
# PARAMETER attr1 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr2 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr3 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr4 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr5 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr6 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr7 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr8 TYPE COLUMN_SEL DEFAULT EMPTY
# RUNTIME python3

import sys, os
from operator import itemgetter

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('output.tsv', base('input.tsv', '*.rel.tsv'),
     ins = 'glue',
     ext = 'rel.tsv')

if not newattr.isidentifier(): # approximately - not quite right
    print('Not allowed as attribute name: {!r}'
          .format(newattr),
          file = sys.stderr)
    exit(1)

gluechar = dict(space = ' ',
                colon = ':',
                hyphen = '-',
                slash = '/')[glue]

attrs = [ attr for attr in (attr1, attr2, attr3, attr4,
                            attr5, attr6, attr7, attr8)
          if attr not in ("EMPTY", "") ]

if len(attrs) < 2:
    # yes, none or one would make sense mathematically
    # but would be a special case (itemgetter),
    # and probably would not make sense to the user
    print('Need at least two attributes to glue',
          file = sys.stderr)
    exit(1)

with open('input.tsv', encoding = 'UTF-8') as data, \
     open('output.tmp', mode = 'w', encoding = 'UTF-8') as out:
    head = next(data).rstrip('\n').split('\t')
    value = itemgetter(*map(head.index, attrs))

    if newattr in head:
        print('Attribute name already used: {!r}'
              .format(newattr),
              file = sys.stderr)
        exit(1)

    print(newattr, *head, sep = '\t', file = out)
    for line in data:
        record = line.rstrip('\n').split('\t')
        print(gluechar.join(value(record)), *record,
              sep = '\t', file = out)

os.rename('output.tmp', 'output.tsv')
