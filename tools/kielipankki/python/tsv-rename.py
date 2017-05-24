# TOOL tsv-rename.py: "Rename TSV fields"
# (Rename TSV fields)
# INPUT old.tsv TYPE GENERIC
# OUTPUT new.tsv
# PARAMETER          old0 TYPE STRING
# PARAMETER          new0 TYPE STRING
# PARAMETER OPTIONAL old1 TYPE STRING
# PARAMETER OPTIONAL new1 TYPE STRING
# PARAMETER OPTIONAL old2 TYPE STRING
# PARAMETER OPTIONAL new2 TYPE STRING
# PARAMETER OPTIONAL old3 TYPE STRING
# PARAMETER OPTIONAL new3 TYPE STRING
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('new.tsv', names.replace('old.tsv', '-ren.tsv'))

olds = (old0, old1, old2, old3)
news = (new0, new1, new2, new3)

for old, new in zip(olds, news):
    if bool(old) == bool(new): continue
    print('bad map', repr(old), '=>', repr(new),
          file = sys.stderr)
    exit(1)

mappin = dict(zip(filter(None, olds), filter(None, news)))

with open('old.tsv') as oldfile:
    oldhead = next(oldfile).rstrip('\n').split('\t')

    for old in mappin:
        if old not in oldhead:
            print('no such field', repr(old), file = sys.stderr)
            print('in', oldhead, file = sys.stderr)
            exit(1)

    newhead = tuple(mappin.get(old, old) for old in oldhead)
    if len(set(newhead)) < len(newhead):
        print('ambiguity in', newhead, file = sys.stderr)
        exit(1)

    with open('new.tmp', mode = 'w', encoding = 'utf-8') as newfile:
        print(*newhead, sep = '\t', file = newfile)
        for line in oldfile:
            print(line, end = '', file = newfile)

os.rename('new.tmp', 'new.tsv')
