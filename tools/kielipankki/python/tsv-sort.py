# TOOL tsv-sort.py: "Sort relation" (Sort records by selected attributes)
# INPUT input.tsv TYPE GENERIC
# OUTPUT output.tsv
# PARAMETER attr1 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr2 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr3 TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER attr4 TYPE COLUMN_SEL DEFAULT EMPTY
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import name, base
from lib_sortedtsv import save

name('output.tsv', base('input.tsv', '*.rel.tsv'),
     ins = 'sorted',
     ext = 'rel.tsv')

with open('input.tsv', encoding = 'UTF-8') as source:
    head = next(source).rstrip('\n').split('\t')

keys = tuple(key for key in (attr1, attr2, attr3, attr4)
             if key not in ('EMPTY', ''))

if not keys:
    print('no attributes selected', file = sys.stderr)
    exit(1)

try:
    save('input.tsv', 'output.tmp', *keys)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

os.rename('output.tmp', 'output.tsv')
