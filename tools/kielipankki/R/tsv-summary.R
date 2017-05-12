# TOOL tsv-summary.R: "Summary of a headed TSV frame)"
# (Uses R to summarize the TSV-form data frame) 
# INPUT table.tsv TYPE GENERIC
# OUTPUT table-summary.txt

# Mylly renaming machinery for R scripts needs developed.

v <- read.delim('table.tsv')
s <- summary(v)
capture.output(s, file = 'table-summary.txt')
