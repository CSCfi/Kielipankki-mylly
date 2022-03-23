# TOOL tsv-as-csv.py: "TSV as CSV"
# (TSV as Comma-Separated Values)
# INPUT table.tsv: "TSV file" TYPE GENERIC
#     (Tab-Separated Values, with mandatory header)
# OUTPUT table.csv

import csv, json, os, sys
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import name, base

name('table.csv', base('table.tsv', '*.tsv'),
     ext = 'csv')

# Python's default CSV dialect aka excel

with open('table.tmp', mode = 'w', encoding = 'utf-8') as out:
    with open('table.tsv', encoding = 'utf-8') as tsv:
        writer = csv.writer(out)
        for line in tsv:
            writer.writerow(line.rstrip('\n').split('\t'))

os.rename('table.tmp', 'table.csv')
