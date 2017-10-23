# TOOL prop1.R: "One-way proportions" (Reports on the proportions of one factor.)
# INPUT data.tsv: "Input data" TYPE GENERIC
# OUTPUT prop.txt: "Report of total proportions"
# OUTPUT summary.txt: "Summary report"
# PARAMETER factoj: "Factor" TYPE COLUMN_SEL
# PARAMETER counts: "Optional count" TYPE COLUMN_SEL

if (counts == "EMPTY") counts <- ""

source(paste(chipster.module.path, "R", "lib_names2.R",  sep = "/"))
source(paste(chipster.module.path, "R", "lib_ratsv.R",  sep = "/"))

name("prop.txt", base("data.tsv", "*.tsv"),
     ins = "prop",
     ext = "txt")

name("summary.txt", base("data.tsv", "*.tsv"),
     ins = "summary",
     ext = "txt")

# data need not be a relation but the reader - it was written;
# counts vanish if counts == "" - R!
data <- read.ra.tsv("data.tsv", setNames(list("integer"), counts))

trix <-
    if (counts == "") { # what a language
        table(data[[factoj]], dnn = factoj)
    } else
        xtabs(substitute(foo ~ bar,
	                 list(foo = as.name(counts),
			      bar = as.name(factoj))),
	      data = data)

# trix[1:5,]

# proportions of total
out <- file("prop.txt", encoding = "UTF-8")
sink(out, type = "output")
sink(out, type = "message")
cat("# Total proportions by prop.table(-)\n")
cat("# Factor:", factoj, "\n")
if (counts != "") cat("# Counts:", counts, "\n")
cat("\n")
prop.table(trix)
sink(type = "output")
sink(type = "message")

# summary - number of cases
out <- file("summary.txt", encoding = "UTF-8")
sink(out, type = "output")
sink(out, type = "message")
cat("# Summary by summary(-)\n")
cat("# Factor:", factoj, "\n")
if (counts != "") cat("# Counts:", counts, "\n")
cat("\n")
summary(trix)
sink(type = "output")
sink(type = "message")
