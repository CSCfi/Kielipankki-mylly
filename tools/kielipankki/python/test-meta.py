# TOOL test-meta.py: "Test if can have name file" (Test if field-name parameters can be filled in from another file - actual data in vrt.txt and names in a tsv)
# INPUT META data.vrt TYPE GENERIC
# INPUT meta.tsv TYPE GENERIC
# OUTPUT out.txt
# PARAMETER name1: "first name" TYPE COLUMN_SEL
# PARAMETER name2: "second name" TYPE COLUMN_SEL
# RUNTIME python3

with open('out.txt', 'w', encoding = 'UTF-8') as out:
    print('name1 ==', name1, file = out)
    print('name2 ==', name2, file = out)
