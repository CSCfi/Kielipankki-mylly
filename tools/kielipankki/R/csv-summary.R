# TOOL csv-summary.R: "Summary of a headed CSV frame)"
# (Uses R to summarize the CSV-form data frame) 
# INPUT table.csv TYPE GENERIC
# OUTPUT table-summary.txt

# Mylly renaming machinery for R scripts needs developed.

v <- read.delim('table.csv')
s <- summary(v)
capture.output(s, file = 'table-summary.txt')
