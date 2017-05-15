# TOOL tsv-as-csv.py: "TSV to CSV"
# (Reformat TSV as CSV.)
# INPUT table.tsv TYPE GENERIC
# OUTPUT table.csv
# RUNTIME python3

import csv, json, os, sys
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('table.tsv', names.replace('table.csv', '.csv'))

with open('table.tmp', mode = 'w', encoding = 'utf-8') as out:
    with open('table.tsv', encoding = 'utf-8') as tsv:
        writer = csv.writer(out)
        for line in tsv:
            writer.writerow(line.rstrip('\n').split('\t')

os.rename('table.tmp', 'table.csv')
