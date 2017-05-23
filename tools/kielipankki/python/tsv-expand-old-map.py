# TOOL tsv-expand-old-map.py: "Extend TSV from a key_value|... field"
# (Extend each record in the TSV by expanding a key-value mapping given in the record. Non-empty maps must contain key_value pairs separated by vertical bars, with no duplicate keys. The default is to extend with all such keys found in the whole TSV.)
# INPUT narrow.tsv TYPE GENERIC
# OUTPUT wide.tsv
# PARAMETER source TYPE STRING DEFAULT "msd"
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
import lib_names as names

names.output('wide.tsv', names.replace('narrow.tsv', '-expand.tsv'))

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

keys = set(filter(None, (key0, key1, key2, key3,
                         key4, key5, key6, key7,
                         key8, key9, keyA, keyB,
                         keyC, keyD, keyE, keyF)))

if not keys:
    with open('narrow.tsv') as narrow:
        head = next(narrow).rstrip('\n').split('\t')
        k = head.index(source)
        keys = set(key
                   for line in narrow
                   for it in [line.rstrip('\n').split('\t')[k]]
                   if it not in ('_', '')
                   for key, val in ( kv.split('_', 1) for kv in it.split('|') ))
                   
# should check that keys not intersect with head (that be an error)

ext = tuple(keys)

with open('wide.tmp', mode = 'w', encoding = 'utf-8') as out:
    with open('narrow.tsv') as narrow:
        head = next(narrow).rstrip('\n').split('\t')
        print(*chain(ext, head), sep = '\t', file = out)
        k = head.index(source)
        for line in narrow:
            record = line.rstrip('\n').split('\t')
            new = dict(pair
                       for it in [record[k]]
                       if it not in ('_', '')
                       for pair in ( kv.split('_', 1) for kv in it.split('|') ))
            print(*chain((new.get(key, '_') for key in ext),
                         record),
                  sep = '\t', file = out)

os.rename('wide.tmp', 'wide.tsv')