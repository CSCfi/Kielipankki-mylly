# TOOL tsv-ext-differ.py: "Extend with difference" (Extend each record with indicators of the numerical difference between two selected attributes. The two input numbers must be positive.)
# INPUT input.tsv TYPE GENERIC
# OUTPUT output.tsv
# PARAMETER xname: "first number" TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER yname: "second number" TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER logbase: "logarithm base" TYPE [2, e, 10] DEFAULT 10
# PARAMETER dform: "difference format" TYPE [
#     flo: "full float",
#     dec: "four decimals",
#     int: "integer"
# ] DEFAULT flo
# PARAMETER rform: "ratio format" TYPE [
#     flo: "full float",
#     dec: "four decimals"
# ] DEFAULT flo
# PARAMETER dprefix: "difference prefix" TYPE STRING DEFAULT wM
# PARAMETER rprefix: "ratio prefix" TYPE STRING DEFAULT wM

import sys, os
from operator import itemgetter

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
name('output.tsv', base('input.tsv', '*.rel.tsv'),
     ins = 'diff',
     ext = 'rel.tsv')

# ^_^
if logbase == '2':
    from math import log2 as log
elif logbase == 'e':
    from math import log as log
elif logbase == '10':
    from math import log10 as log
else:
    print('this cannot happen', file = sys.stderr)
    exit(1)

if dform == 'flo':
    def dformat(x): return x
elif dform == 'dec':
    def dformat(x): return '{:.4f}'.format(x)
elif dform == 'int':
    def dformat(x): return int(x)
else:
    print('incomplete case analysis', file = sys.stderr)
    exit(1)

if rform == 'flo':
    def rformat(x): return x
elif rform == 'dec':
    def rformat(x): return '{:.4f}'.format(x)
else:
    print('incomplete case analysis', file = sys.stderr)
    exit(1)

# direct and absolute difference
# direct and absolute log ratio aka difference of logs
ddname = '{}dif'.format(dprefix)
adname = '{}adif'.format(dprefix)
drname = '{}diflog'.format(rprefix)
arname = '{}adiflog'.format(rprefix)

try:
    with open('input.tsv', encoding = 'UTF-8') as data, \
         open('output.tmp', mode = 'w', encoding = 'UTF-8') as out:
        head = next(data).rstrip('\n').split('\t')
        if any((attr in head) for attr in (ddname, adname, drname, arname)):
            print('attribute name already in use', file = sys.stderr)
            print('consider a different prefix', file = sys.stderr)
            exit(1)
        getx = itemgetter(head.index(xname))
        gety = itemgetter(head.index(yname))
        print(ddname, adname, drname, arname, *head,
              sep = '\t', file = out)
        for line in data:
            record = line.rstrip('\n').split('\t')
            x = float(getx(record))
            y = float(gety(record))
            print(dformat(x - y), dformat(abs(x - y)),
                  rformat(log(x/y)), rformat(abs(log(x/y))),
                  *record,
                  sep = '\t', file = out)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

os.rename('output.tmp', 'output.tsv')
