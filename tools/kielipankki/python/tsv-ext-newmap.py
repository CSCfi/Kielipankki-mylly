# TOOL tsv-ext-newmap.py: "Extend relation from a key=value,... field"
# (Extend each record in by expanding a key-value mapping in one of its attributes. Non-empty maps must contain key=value pairs separated by commas, with no duplicate keys. The default is to extend with all such keys found in the whole relation.)
# INPUT narrow.tsv TYPE GENERIC
# OUTPUT wide.tsv
# PARAMETER source TYPE COLUMN_SEL DEFAULT "EMPTY"
# PARAMETER OPTIONAL key0 TYPE STRING
# PARAMETER OPTIONAL key1 TYPE STRING
# PARAMETER OPTIONAL key2 TYPE STRING
# PARAMETER OPTIONAL key3 TYPE STRING
# PARAMETER OPTIONAL key4 TYPE STRING
# PARAMETER OPTIONAL key5 TYPE STRING
# PARAMETER OPTIONAL key6 TYPE STRING
# PARAMETER OPTIONAL key7 TYPE STRING
# PARAMETER OPTIONAL key8 TYPE STRING
# PARAMETER OPTIONAL key9 TYPE STRING
# PARAMETER OPTIONAL keyA TYPE STRING
# PARAMETER OPTIONAL keyB TYPE STRING
# PARAMETER OPTIONAL keyC TYPE STRING
# PARAMETER OPTIONAL keyD TYPE STRING
# PARAMETER OPTIONAL keyE TYPE STRING
# PARAMETER OPTIONAL keyF TYPE STRING
# RUNTIME python3

# The "old" refers to the "key_value|..." format.
# The "new" format will be "key=value,..." of UD.

from itertools import chain
import os

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

name('wide.tsv', base('narrow.tsv', '*.rel.tsv'),
     ins = 'expand',
     ext = 'rel.tsv')

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

keys = set(filter(None, (key0, key1, key2, key3,
                         key4, key5, key6, key7,
                         key8, key9, keyA, keyB,
                         keyC, keyD, keyE, keyF)))

if not keys:
    with open('narrow.tsv', encoding = 'UTF-8') as narrow:
        head = next(narrow).rstrip('\n').split('\t')
        k = head.index(source)
        keys = set(key
                   for line in narrow
                   for it in [line.rstrip('\n').split('\t')[k]]
                   if it not in ('_', '')
                   for key, val in ( kv.split('=', 1) for kv in it.split(',') ))

if keys & set(head):
    print('new keys conflict with old keys', file = sys.stderr)
    print('conflicting keys:', *(keys & set(head)), file = sys.stderr)
    exit(1)

ext = tuple(keys)

with open('wide.tmp', mode = 'w', encoding = 'UTF-8') as out:
    with open('narrow.tsv', encoding = 'UTF-8') as narrow:
        head = next(narrow).rstrip('\n').split('\t')
        print(*chain(ext, head), sep = '\t', file = out)
        k = head.index(source)
        for line in narrow:
            record = line.rstrip('\n').split('\t')
            new = dict(pair
                       for it in [record[k]]
                       if it not in ('_', '')
                       for pair in ( kv.split('=', 1) for kv in it.split(',') ))
            print(*chain((new.get(key, '_') for key in ext),
                         record),
                  sep = '\t', file = out)

os.rename('wide.tmp', 'wide.tsv')
