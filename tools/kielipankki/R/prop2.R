# TOOL prop2.R: "Two-way proportions" (Reports on the proportions of two factors.)
# INPUT data.tsv: "Input data" TYPE GENERIC
# OUTPUT prop-tot.txt: "Report of total proportions"
# OUTPUT prop-row.txt: "Report of row proportions"
# OUTPUT prop-col.txt: "Report of column proportions"
# OUTPUT summary.txt: "Summary report"
# PARAMETER factor1: "Row factor" TYPE COLUMN_SEL
# PARAMETER factor2: "Column factor" TYPE COLUMN_SEL
# PARAMETER counts: "Optional count" TYPE COLUMN_SEL

if (counts == "EMPTY") counts <- ""

source(paste(chipster.module.path, "R", "lib_names2.R",  sep = "/"))
source(paste(chipster.module.path, "R", "lib_ratsv.R",  sep = "/"))

name("prop-tot.txt", base("data.tsv", "*.tsv"),
     ins = "prop-tot",
     ext = "txt")

name("prop-row.txt", base("data.tsv", "*.tsv"),
     ins = "prop-row",
     ext = "txt")

name("prop-col.txt", base("data.tsv", "*.tsv"),
     ins = "prop-col",
     ext = "txt")

name("summary.txt", base("data.tsv", "*.tsv"),
     ins = "summary",
     ext = "txt")

# data need not be a relation but the reader - it was written;
# counts vanish if counts == "" - R!
data <- read.ra.tsv("data.tsv", setNames(list("integer"), counts))

trix <-
    if (counts == "") { # what a language
        table(data[[factor1]], data[[factor2]], dnn = c(factor1, factor2))
    } else
        xtabs(substitute(foo ~ bar + baz,
	                 list(foo = as.name(counts),
			      bar = as.name(factor1),
			      baz = as.name(factor2))),
	      data = data)

# trix[1:5,]

# proportions of total
out <- file("prop-tot.txt", encoding = "UTF-8")
sink(out, type = "output")
sink(out, type = "message")
cat("# Total proportions by prop.table(-)\n")
cat("# Row factor:", factor1, "\n")
cat("# Col factor:", factor2, "\n")
if (counts != "") cat("# Counts:", counts, "\n")
cat("\n")
prop.table(trix)
sink(type = "output")
sink(type = "message")

# proportions of row sums
out <- file("prop-row.txt", encoding = "UTF-8")
sink(out, type = "output")
sink(out, type = "message")
cat("# Row proportions by prop.table(-, 1)\n")
cat("# Row factor:", factor1, "\n")
cat("# Col factor:", factor2, "\n")
if (counts != "") cat("# Counts:", counts, "\n")
cat("\n")
prop.table(trix, 1)
sink(type = "output")
sink(type = "message")

# proportions of column sums
out <- file("prop-col.txt", encoding = "UTF-8")
sink(out, type = "output")
sink(out, type = "message")
cat("# Column proportions by prop.table(-, 2)\n")
cat("# Row factor:", factor1, "\n")
cat("# Col factor:", factor2, "\n")
if (counts != "") cat("# Counts:", counts, "\n")
cat("\n")
prop.table(trix, 2)
sink(type = "output")
sink(type = "message")

# summary - chi-squared independence test
out <- file("summary.txt", encoding = "UTF-8")
sink(out, type = "output")
sink(out, type = "message")
cat("# Summary by summary(-)\n")
cat("# Row factor:", factor1, "\n")
cat("# Col factor:", factor2, "\n")
if (counts != "") cat("# Counts:", counts, "\n")
cat("\n")
summary(trix)
sink(type = "output")
sink(type = "message")
