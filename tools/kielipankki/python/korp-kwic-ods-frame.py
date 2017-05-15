# TOOL korp-kwic-ods-frame.py: "DEPRECATED Korp KWIC to ODS Frame"
# (DEPRECATED Flatten a JSON concordance in ODS form, with header.)
# INPUT kwic.json TYPE GENERIC
# OUTPUT kwic.ods
# RUNTIME python3

'''Turn JSON format KWIC concordance from Korp API to a flat, headed
   Open Document Spreadsheet. Use the attribute names from the input
   KWIC for the output columns. Repeat structural attributes of a hit
   for each token.

'''

# installed odf for self so
# pip3 install --user odfpy
# waiting for Martin to hopefully install libraries for Mylly user

import json, odf, os, sys
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('kwic.ods', names.replace('kwic.json', '.ods'))

# extract the writing from
# https://github.com/eea/odfpy/blob/master/csv2ods/csv2ods which
# mainly deals with Python2 compatibility, option parsing, reading
# CSV, and guessing character encodings and cell styles :/
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

with open('kwic.json', encoding = 'utf-8') as f:
    data = json.load(f)

kwic = data['kwic']

# lead sentence/token determines which attributes,
# any CoNLL equivalents first,
# then match and corpus,
# then a couple of our own,
# then other positionals lexicographically
# then structurals lexicographically

lead = kwic[0]['tokens'][0] # lead token
head = [ key
         for key in 'ref word lemma pos msd dephead deprel'.split()
         if key in lead ]

what = 'match_start', 'match_end', 'corpus' # hope them is free!

rest = [ key for key in sorted(lead) if key not in head ]
meta = sorted(kwic[0]['structs'])

# is there something wrong about the match start and end?
# also, should they be just 0/1 anyway?
# also, should there also be a hit counter?

# Begins!

textdoc = OpenDocumentSpreadsheet()

# Create a style for the table content. One we can modify later in the
# word processor. [Copied this from csv2ods - is this even useful?
# does there need to be a style? find out!]
tablecontents = Style(name="Table Contents", family="paragraph")
tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
tablecontents.addElement(TextProperties(fontweight="bold"))
textdoc.styles.addElement(tablecontents)

table = Table(name = 'kwic')

hr = TableRow()
table.addElement(hr)
for name in chain(head, what, rest, meta):
    hc = TableCell(valuetype = "string")
    hr.addElement(hc)
    p = P(stylename = tablecontents, text = name) # is this right?
    hc.addElement(p)

for hit in kwic:
    for token in hit['tokens']:
        tr = TableRow()
        table.addElement(tr)
        for value in chain((token[key] for key in head),
                           (hit['match']['start'],
                            hit['match']['end'],
                            hit['corpus']),
                           (token[key] for key in rest),
                           (hit['structs'][key] for key in meta)):
            tc = TableCell(valuetype = "string")
            tr.addElement(tc)
            p = P(stylename = tablecontents, text = value) # right?
            tc.addElement(p)

textdoc.spreadsheet.addElement(table)
textdoc.save('kwic.tmp')
os.rename('kwic.tmp', 'kwic.ods')
