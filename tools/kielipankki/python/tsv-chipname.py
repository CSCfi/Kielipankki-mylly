# TOOL tsv-chipname.py: "Rename attributes in 'chip.'"
# (Add 'chip.' prefix to attribute names that already have a numeric prefix.)
# INPUT old.tsv TYPE GENERIC
# OUTPUT new.tsv
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('new.tsv', base('old.tsv', '*.rel.tsv'),
     ins = 'chip',
     ext = 'rel.tsv')

with open('old.tsv') as oldfile:
    oldhead = next(oldfile).rstrip('\n').split('\t')

    newhead = tuple(('chip.' + old
                     if old.startswith(('kM', 'uM', 'wM'))
                     else old)
                    for old in oldhead)

    if len(set(newhead)) < len(newhead):
        print('duplicate name in new head:', file = sys.stderr)
        print(*newhead, file = sys.stderr)
        exit(1)

    with open('new.tmp', mode = 'w', encoding = 'utf-8') as newfile:
        print(*newhead, sep = '\t', file = newfile)
        for line in oldfile:
            print(line, end = '', file = newfile)

os.rename('new.tmp', 'new.tsv')
