# TOOL tsv-requot.py: "Replace ASCII quotes" (Replace all ASCII quotes with right quotes. Preserves relationality if possible.)
# INPUT data.tsv TYPE GENERIC
# OUTPUT result.tsv
# RUNTIME python3

import os, sys
from itertools import groupby

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_sortedtsv import processanyway # no keys, just sort
from lib_names2 import base, name, extension

base('data.tsv', '*.rel.tsv', '*.tsv')
ext = extension('data.tsv', 'rel.tsv', 'tsv')

# 'result.tsv' is named at the end of the script, after checking, if
# input was in *.rel.tsv, whether relationality is preserved - if not,
# drop rel and produce only tsv

reps = str.maketrans(( '\N{QUOTATION MARK}'
                       '\N{APOSTROPHE}' ),
                     ( '\N{RIGHT DOUBLE QUOTATION MARK}'
                       '\N{RIGHT SINGLE QUOTATION MARK}' ))

try:
    with open('data.tsv', encoding = 'UTF-8') as data:
        head = next(data).rstrip('\n').split('\t')
        with open('result.tsv', mode = 'w', encoding = 'UTF-8') as out:
            print(*head, sep = '\t', file = out)
            for count, line in enumerate(data, start = 1):
                print(line.translate(reps),
                      sep = '\t',
                      end = '',
                      file = out)
except Exception as exn:
    print(exn, file = sys.stderr)
    exit(1)

if ext == 'rel.tsv':

    # check if relationality is preserved;
    # if not, drop rel and produce mere tsv

    def discount(ins):
        global ucount
        for unique, _ in enumerate(groupby(ins), start = 1):
            pass
        else:
            ucount = unique

    ucount = None
    processanyway('result.tsv', discount)

    if ucount < count:
        ext = 'tsv'

name('result.tsv', base('data.tsv', '*.rel.tsv', '*.tsv'),
     ins = 'requot',
     ext = ext)
