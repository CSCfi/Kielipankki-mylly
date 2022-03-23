# TOOL tsv-sort.py: "Sort records" (Sort records by selected attributes)
# INPUT input.tsv TYPE GENERIC
# OUTPUT output.tsv
# PARAMETER attr1 TYPE COLUMN_SEL
# PARAMETER kind1 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER sign1 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER OPTIONAL attr2 TYPE COLUMN_SEL
# PARAMETER OPTIONAL kind2 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER OPTIONAL sign2 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER OPTIONAL attr3 TYPE COLUMN_SEL
# PARAMETER OPTIONAL kind3 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER OPTIONAL sign3 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER OPTIONAL attr4 TYPE COLUMN_SEL
# PARAMETER OPTIONAL kind4 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER OPTIONAL sign4 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER OPTIONAL attr5 TYPE COLUMN_SEL
# PARAMETER OPTIONAL kind5 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER OPTIONAL sign5 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER OPTIONAL attr6 TYPE COLUMN_SEL
# PARAMETER OPTIONAL kind6 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER OPTIONAL sign6 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER OPTIONAL attr7 TYPE COLUMN_SEL
# PARAMETER OPTIONAL kind7 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER OPTIONAL sign7 TYPE [ "increasing", "decreasing" ] DEFAULT increasing
# PARAMETER OPTIONAL attr8 TYPE COLUMN_SEL
# PARAMETER OPTIONAL kind8 TYPE [ "default", "integer", "float", "string" ] DEFAULT default
# PARAMETER OPTIONAL sign8 TYPE [ "increasing", "decreasing" ] DEFAULT increasing

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import name, base, extension
from lib_sortedtsv import save

name('output.tsv', base('input.tsv', '*.rel.tsv', '*.tsv'),
     ins = 'sorted',
     ext = extension('input.tsv', 'rel.tsv', 'tsv'))

keys = tuple((attr, kind, sign)
             for (attr, kind, sign)
             in zip((attr1, attr2, attr3, attr4, attr5, attr6, attr7, attr8),
                    (kind1, kind2, kind3, kind4, kind5, kind6, kind7, kind8),
                    (sign1, sign2, sign3, sign4, sign5, sign6, sign7, sign8))
             if attr)

try:
    save('input.tsv', 'output.tmp', *keys)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

os.rename('output.tmp', 'output.tsv')
