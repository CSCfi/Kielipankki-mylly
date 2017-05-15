# TOOL tsv-as-ods.py: "TSV as ODS"
# (TSV as ODS aka Open Document Spreadsheet)
# INPUT table.tsv TYPE GENERIC
# OUTPUT table.ods
# RUNTIME python3

# depends on odf (from odfpy)

import odf, os, sys
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('table.ods', names.replace('table.tsv', '.ods'))

# extract the writing from
# https://github.com/eea/odfpy/blob/master/csv2ods/csv2ods which
# mainly deals with Python2 compatibility, option parsing, reading
# CSV, and guessing character encodings and cell styles :/
from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

textdoc = OpenDocumentSpreadsheet()

# Create a style for the table content. One we can modify later in the
# word processor. [Copied this from csv2ods - is this even useful?
# does there need to be a style? find out!]
tablecontents = Style(name="Table Contents", family="paragraph")
tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
tablecontents.addElement(TextProperties(fontweight="bold"))
textdoc.styles.addElement(tablecontents)

table = Table(name = 'table')

with open('table.tsv', encoding = 'utf-8') as tsv:
    # header
    head = next(tsv).rstrip('\n').split('\t')
    hr = TableRow()
    table.addElement(hr)
    for name in head:
        hc = TableCell(valuetype = "string")
        hr.addElement(hc)
        p = P(stylename = tablecontents, text = name) # is this right?
        hc.addElement(p)
    # records
    for line in tsv:
        record = line.rstrip('\n').split('\t')
        tr = TableRow()
        table.addElement(tr)
        for value in record:
            tc = TableCell(valuetype = "string")
            tr.addElement(tc)
            p = P(stylename = tablecontents, text = value) # right?
            tc.addElement(p)

textdoc.spreadsheet.addElement(table)
textdoc.save('table.tmp')
os.rename('table.tmp', 'table.ods')
