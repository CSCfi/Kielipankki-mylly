# TOOL tsv-as-ods.py: "TSV as ODS"
# (TSV as Open Document Spreadsheet. Column name prefix cM or kM indicates that cells contain whole numbers, like counts, and wM or vM indicates a numeric weight.)
# INPUT table.tsv TYPE GENERIC
# OUTPUT table.ods
# RUNTIME python3

import odf, os, sys # depends on odf (package odfpy from PyPI)

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('table.ods', names.replace('table.tsv', '.ods'))

from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableHeaderRows, TableRow, TableCell

sheet = OpenDocumentSpreadsheet()

# We would like to attach "common" styles for different kinds of data
# columns in the table (and for head cells, why not) for the user to
# modify in their ODS "consumer", but the principal consumer does not
# seem to support common styles properly. (Maybe the latest version,
# though? Or a future version? Or some other consumer altogether?)

# See https://github.com/eea/odfpy/blob/master/csv2ods/csv2ods for how
# one attaches common styles to a spreadsheet document in odfpy. (It
# deals mainly with Python2 compatibility, option parsing, reading
# CSV, and guessing character encodings and cell styles :/ Oh well.)

table = Table(name = 'table')

def floatcell(value):
    # should have a number style in table:column to make it show as a
    # "number" or a "decimal number" or a "scientific number" but for
    # now, the principal consumer may not use it right; on the other
    # hand, it seems to guess nicely, hopefully, maybe
    return TableCell(valuetype = "float", value = value)

def stringcell(value):
    # header table:table-row should also have a suitable default style
    return TableCell(valuetype = "string", stringvalue = value)

def row(headmap, record):
    result = TableRow()
    for make, value in zip(headmap, record):
        result.addElement(make(value))
    return result

with open('table.tsv', encoding = 'utf-8') as tsv:
    # header from first line
    head = next(tsv).rstrip('\n').split('\t')
    # (this is where we would insert default cell styles for the
    # columns)
    headrows = TableHeaderRows()
    headrow = TableRow()
    for name in head:
        headrow.addElement(stringcell(name))
    headrows.addElement(headrow)
    table.addElement(headrows)
    # empty row before data rows helps select data rows at least for
    # sorting at least in an oldish LibreOffice (one can hide it)
    table.addElement(TableRow())
    # records
    headmap = [ (floatcell if name.startswith(('cM', 'kM', 'wM', 'vM'))
                 else stringcell)
                for name in head ]
    for line in tsv:
        record = line.rstrip('\n').split('\t')
        table.addElement(row(headmap, record))

sheet.spreadsheet.addElement(table)
sheet.save('table.tmp')
os.rename('table.tmp', 'table.ods')
