# TOOL tsv-rename.py: "Rename attributes"
# (Rename selected attributes. EMPTY is not a name.)
# INPUT old.tsv TYPE GENERIC
# OUTPUT new.tsv
# PARAMETER          old0: "old name" TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER          new0: "new name" TYPE STRING
# PARAMETER OPTIONAL old1: "old name" TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL new1: "new name" TYPE STRING
# PARAMETER OPTIONAL old2: "old name" TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL new2: "new name" TYPE STRING
# PARAMETER OPTIONAL old3: "old name" TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL new3: "new name" TYPE STRING
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('new.tsv', base('old.tsv', '*.rel.tsv'),
     ins = 'rename',
     ext = 'rel.tsv')

olds = (old0, old1, old2, old3)
news = (new0, new1, new2, new3)

for old, new in zip(olds, news):
    if (old in ("EMPTY", "")) == (new in ("EMPTY", "")): continue
    print('bad renaming:', repr(old), '=>', repr(new),
          file = sys.stderr)
    exit(1)

mappin = dict((old, new) for old, new in zip(olds, news)
              if old not in ("EMPTY", ""))

with open('old.tsv') as oldfile:
    oldhead = next(oldfile).rstrip('\n').split('\t')

    for old in mappin:
        if old not in oldhead:
            print('no such field', repr(old), file = sys.stderr)
            print('in', oldhead, file = sys.stderr)
            exit(1)

    newhead = tuple(mappin.get(old, old) for old in oldhead)

    if len(set(newhead)) < len(newhead):
        print('duplicate name in new head:', file = sys.stderr)
        print(*newhead, file = sys.stderr)
        exit(1)

    with open('new.tmp', mode = 'w', encoding = 'utf-8') as newfile:
        print(*newhead, sep = '\t', file = newfile)
        for line in oldfile:
            print(line, end = '', file = newfile)

os.rename('new.tmp', 'new.tsv')
