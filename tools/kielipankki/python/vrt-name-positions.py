# TOOL vrt-name-positions.py: "Name fields" (Name some fields. Default field names are V1, V2, ...)
# INPUT input.vrt TYPE GENERIC
# OUTPUT output.vrt
# PARAMETER pos1 TYPE STRING DEFAULT EMPTY
# PARAMETER pos2 TYPE STRING DEFAULT EMPTY
# PARAMETER pos3 TYPE STRING DEFAULT EMPTY
# PARAMETER pos4 TYPE STRING DEFAULT EMPTY
# PARAMETER pos5 TYPE STRING DEFAULT EMPTY
# PARAMETER pos6 TYPE STRING DEFAULT EMPTY
# PARAMETER pos7 TYPE STRING DEFAULT EMPTY
# PARAMETER pos8 TYPE STRING DEFAULT EMPTY
# PARAMETER pos9 TYPE STRING DEFAULT EMPTY
# PARAMETER pos10 TYPE STRING DEFAULT EMPTY
# PARAMETER pos11 TYPE STRING DEFAULT EMPTY
# PARAMETER pos12 TYPE STRING DEFAULT EMPTY
# RUNTIME python3

import os, sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('output.vrt', base('input.vrt', '*.vrt', '*.vrt.txt'),
     ext = 'vrt.txt')

with open('input.vrt', encoding = 'UTF-8') as source:
    # Finding the first line that gives input names, either explicitly
    # in the form of the comment or implicitly as a record, whichever
    # comes first.
    lines = (line for line in source
             if ((line.startswith('<!-- Positional attributes:')
                  or not (line.startswith('<')))
                 and not line.isspace()))
    line = next(lines, None)

mapping = [ ('' if pos in ('', 'EMPTY') else pos)
            for pos in (pos1, pos2, pos3, pos4, pos5, pos6,
                       pos7, pos8, pos9, pos10, pos11, pos12) ]

# should really just reject any document with no content line, maybe

if line is None and not mapping:
    print('Insufficient information:',
          '- no input names or records',
          '- no mapping',
          sep = '\n', file = sys.stderr)
    exit(1)
elif line is None:
    # make oldnames and mapping the same length
    while mapping and mapping[-1]:
        mapping.pop()
    oldnames = [ 'V{}'.format(k)
                 for k, n in enumerate(mapping, start = 1) ]
elif line.startswith('<'):
    # explicit old names
    head, tail = line.split(':')
    oldnames = tail.split('-')[0].split()
else:
    # implicit old names from a first record
    oldnames = [ 'V{}'.format(k)
                 for k, v in enumerate(line.split('\t'), start = 1) ]

if any(mapping[len(oldnames):]):
    print('names beyond last position', file = sys.stderr)
    print('document has {} fields'.format(len(oldnames)), file = sys.stderr)
    exit(1)

# should really just reject any document with no content line, maybe

newnames = ([ (new or old) for old, new in zip(oldnames, mapping) ]
            or [ 'V1' ])

if len(newnames) > len(set(newnames)):
    print('Duplicate in new names:', *newnames, file = sys.stderr)
    exit(1)

with open('input.vrt', encoding = 'UTF-8') as source, \
     open('output.tmp', 'w', encoding = 'UTF-8') as target:
    print('<!-- Positional attributes: {} -->'.format(' '.join(newnames)),
          file = target)
    for line in source:
        if line.startswith('<!-- Positional attributes:'):
            continue
        else:
            print(line, end = '', file = target)

os.rename('output.tmp', 'output.vrt')
