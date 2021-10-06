# TOOL tiny-tsv.py: "Make tiny relation"
# (Make a relation of up to three records of one to three attributes)
# OUTPUT tiny.tsv
# PARAMETER          attr0 TYPE STRING
# PARAMETER OPTIONAL val00 TYPE STRING
# PARAMETER OPTIONAL val01 TYPE STRING
# PARAMETER OPTIONAL val02 TYPE STRING
# PARAMETER OPTIONAL attr1 TYPE STRING
# PARAMETER OPTIONAL val10 TYPE STRING
# PARAMETER OPTIONAL val11 TYPE STRING
# PARAMETER OPTIONAL val12 TYPE STRING
# PARAMETER OPTIONAL attr2 TYPE STRING
# PARAMETER OPTIONAL val20 TYPE STRING
# PARAMETER OPTIONAL val21 TYPE STRING
# PARAMETER OPTIONAL val22 TYPE STRING
# IMAGE comp-16.04-mylly
# RUNTIME python3

# So it cannot make Dee or Dum. Make separate tools for those two
# if there is demand.

import sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('tiny.tsv', 'tiny', ext = 'rel.tsv')

def fail(mess): print(mess, file = sys.stderr) ; exit(1)

attrs = (attr0, attr1, attr2)
vals0 = (val00, val10, val20)
vals1 = (val01, val11, val21)
vals2 = (val02, val12, val22)
valss = (vals0, vals1, vals2)

if any(bool(attr) < bool(val)
       for vals in valss
       for attr, val in zip(attrs, vals)):
    fail('missing attribute name (some values filled)')

head = tuple(filter(None, attrs))
recs = []
for vals in valss:
    rec = tuple(val for key, val in zip(attrs, vals) if key)
    if any(rec):
        if not all(rec): fail('incomplete record (some values filled)')
        if rec in recs: fail('duplicate record')
        recs.append(rec)

with open('tiny.tsv', mode = 'w', encoding = 'utf-8') as out:
    print(*head, sep = '\t', file = out)
    for rec in recs:
        print(*rec, sep = '\t', file = out)
