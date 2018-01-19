# TOOL tsv-sort.py: "Sort relation" (Sort records by selected attributes)
# INPUT input.tsv TYPE GENERIC
# OUTPUT output.tsv
# PARAMETER attr1 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER kind1 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER sign1 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER attr2 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER kind2 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER sign2 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER attr3 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER kind3 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER sign3 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER attr4 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER kind4 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER sign4 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER attr5 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER kind5 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER sign5 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER attr6 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER kind6 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER sign6 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER attr7 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER kind7 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER sign7 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER attr8 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER kind8 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER sign8 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import name, base
from lib_sortedtsv import save

name('output.tsv', base('input.tsv', '*.rel.tsv'),
     ins = 'sorted',
     ext = 'rel.tsv')

# with open('input.tsv', encoding = 'UTF-8') as source:
#    head = next(source).rstrip('\n').split('\t')

keys = tuple((attr, kind, sign)
             for (attr, kind, sign)
             in zip((attr1, attr2, attr3, attr4, attr5, attr6, attr7, attr8),
                    (kind1, kind2, kind3, kind4, kind5, kind6, kind7, kind8),
                    (sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8))
             if attr not in ('EMPTY', ''))

if not keys:
    print('no attributes selected', file = sys.stderr)
    exit(1)

try:
    save('input.tsv', 'output.tmp', *keys)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

os.rename('output.tmp', 'output.tsv')
