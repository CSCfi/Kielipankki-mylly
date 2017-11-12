# TOOL tsv-sort.py: "Sort relation" ()
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

# actually a mere sort should put its output directly to the file; the
# present pattern is meant for when the output is further processed in
# more interesting ways than merely passing it on
#
# def copy(source):
#    with open('output.tmp', mode = 'w', encoding = 'UTF-8') as out:
#        print(*head, sep = '\t', file = out)
#        for line in source:
#            print(line, end = '', file = out)

keys = tuple(key for key in (attr1, attr2, attr3, attr4)
             if key not in ('EMPTY', ''))
            
try:
    save('input.tsv', 'output.tmp', *keys)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

os.rename('output.tmp', 'output.tsv')
