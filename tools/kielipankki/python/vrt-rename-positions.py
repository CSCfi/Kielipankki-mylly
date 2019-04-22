# TOOL vrt-rename-positions.py: "Rename VRT positions" (Rename some positions. Default input names are v1, v2, ...)
# INPUT input.vrt TYPE GENERIC
# OUTPUT output.vrt
# PARAMETER old1 TYPE STRING DEFAULT EMPTY
# PARAMETER new1 TYPE STRING DEFAULT EMPTY
# PARAMETER old2 TYPE STRING DEFAULT EMPTY
# PARAMETER new2 TYPE STRING DEFAULT EMPTY
# PARAMETER old3 TYPE STRING DEFAULT EMPTY
# PARAMETER new3 TYPE STRING DEFAULT EMPTY
# PARAMETER old4 TYPE STRING DEFAULT EMPTY
# PARAMETER new4 TYPE STRING DEFAULT EMPTY
# RUNTIME python3

import html, os, sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.vrt', base('input.vrt', '*.vrt', '*.vrt.txt'),
     ext = 'vrt.txt')

with open('input.vrt', encoding = 'UTF-8') as source:
    # Finding the first line that gives input names, either explicitly
    # in the form of the comment or implicitly as a record, whichever
    # comes first.
    lines = (line for line in source
             if ((line.startswith('<!-- #vrt positional-attributes:')
                  or not (line.startswith('<')))
                 and not line.isspace()))
    line = next(lines, None)

mapping = dict((old, (old if new in ('', 'EMPTY') else new))
               for (old, new) in ((old1, new1),
                                  (old2, new2),
                                  (old3, new3),
                                  (old4, new4))
               if old not in ('', 'EMPTY'))

# should really just reject any document with no content line, maybe

if line is None and not mapping:
    print('Insufficient information:',
          '- no input names or records',
          '- no mapping',
          sep = '\n',
          file = sys.stderr)
    exit(1)
elif line is None:
    try:
        highest = max(int(old.strip('v')) for old in mapping)
        if not (0 < highest < 30): raise Exception()
        oldnames = [ 'v{}'.format(k + 1) for k in range(highest) ]
    except Exception:
        print('Insufficient information:',
              '- no input names or records',
              '- with mapping not in default name form',
              sep = '\n', file = sys.stderr)
        exit(1)
elif line.startswith('<'):
    # explicit old names
    head, tail = line.split(':')
    oldnames = tail.rstrip(' ->\r\n')
else:
    # implicit old names from a first record
    oldnames = [ 'v{}'.format(k)
                 for k, v in enumerate(line.split('\t'), start = 1) ]

try:
    newnames = [ mapping.get(name, name) for name in oldnames ]
except Exception:
    print('No such input name', file = sys.stderr)
    exit(1)

if len(newnames) > len(set(newnames)):
    print('Duplicate in new names:', *newnames, file = sys.stderr)
    exit(1)

with open('input.vrt', encoding = 'UTF-8') as source, \
     open('output.tmp', 'w', encoding = 'UTF-8') as target:
    print('<!-- #vrt positional-attributes: {} -->'
          .format(' '.join(newnames)),
          file = target)
    for line in source:
        if line.startswith('<!-- #vrt positional-attributes:'):
            continue
        else:
            print(line, end = '', file = target)

os.rename('output.tmp', 'output.vrt')
