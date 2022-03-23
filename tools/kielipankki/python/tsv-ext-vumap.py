# TOOL tsv-ext-vumap.py: "Extend from key_value|..."
# (Extend each record from a key-value attribute. A non-empty map contains key_value pairs separated by vertical bars, with no duplicate keys. The default is to extend with those keys that occur.)
# INPUT narrow.tsv TYPE GENERIC
# OUTPUT wide.tsv
# PARAMETER source TYPE COLUMN_SEL
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

# The "vu" refers to the "key_value|..." format:
# v for the vertical bar,
# u for the underscore.

import os

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name, extension
from lib_extmap import scan, extend

name('wide.tsv', base('narrow.tsv', '*.rel.tsv', '*.tsv'),
     ins = 'ext-map',
     ext = extension('narrow.tsv', 'rel.tsv', 'tsv'))

keys = scan('narrow.tsv', source, '|', '_',
            tuple(key for key in (key0, key1, key2, key3,
                                  key4, key5, key6, key7,
                                  key8, key9, keyA, keyB,
                                  keyC, keyD, keyE, keyF)
                  if key))

extend('narrow.tsv', 'wide.tmp', source, '|', '_', keys)

os.rename('wide.tmp', 'wide.tsv')
