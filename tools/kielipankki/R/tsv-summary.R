# TOOL tsv-summary.R: "Summarize TSV using R"
# (Uses R for a rough summary of a TSV file) 
# INPUT table.tsv TYPE GENERIC
# OUTPUT summary.txt

# Mylly renaming machinery for R scripts needs developed.

v <- read.delim('table.tsv', quote = '')
s <- summary(v)
capture.output(s, file = 'summary.txt')
