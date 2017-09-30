# TOOL test-colsel.py: "Test COLUMN_SEL parameter"
#     (Test Chipster tool interface parameter type COLUMN_SEL,
#      now with two required files to see if union or intersection
#      of names becomes available, or what. Ok it only show the
#      first set. Good enough?)
# INPUT some.tsv TYPE GENERIC (Whatever TSV file. TSV file has column names.)
# INPUT more.tsv TYPE GENERIC (Whatever another TSV file.)
# OUTPUT info.txt  (File attempts to reveal parameters)
# PARAMETER col1: "First column name" TYPE COLUMN_SEL (Column in input file)
# PARAMETER col2: "Nothe column name" TYPE COLUMN_SEL (Column in input file)
# PARAMETER col3: "Anoth column name" TYPE COLUMN_SEL (Column in input file)
# RUNTIME python3

# Want to run this in Chipster and see
# - how one gets to select column name in the user interface

with open('info.txt', 'wt') as f:
    print('one column:', repr(col1), file = f)
    print('two column:', repr(col2), sep = '\t', file = f)
    print('yet anothe:', repr(col3), sep = '\t', file = f)
    print(file = f)
