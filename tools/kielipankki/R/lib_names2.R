# Source this in a Mylly tool script and then specify
# output file names based on inputs like in this example:
#
# name("result", base("datami", "*.rel.tsv"),
#      ext = "pdf")
#
# requires: datami => jotain.omaa.rel.tsv in chipster-inputs.tsv
# produces: result => jotain.pdf in chipster-outputs.tsv
#
# There is also an optional parameter ins to insert a middle part.

base <- function (argname, pattern) {
    cash <- read.table("chipster-inputs.tsv", colClasses = "character")
    # is not a cache because not sure how to do that in R - never mind
    
    name <- cash[cash$V1 == argname,]$V2

    if (length(name) != 1) {
        stop("\n",
             "input name ", argname, " not in chipster-inputs.tsv\n",
	     "or not unique; this cannot happen - please report")
    }

    if (!grepl(glob2rx(pattern), name)) {
        stop("\n",
             "input file name: ", name, "\n",
	     "does not match: ", pattern)
    }

    base <- unlist(strsplit(name, ".", fixed = TRUE))[1]

    if (base == "") {
        # not sure if this can even happen in Chipster
        stop("\n",
	     "input file name: ", name, "\n",
	     "has empty base part")
    }

    base
}

name <- function(resname, base, ins = NULL, ext) {
    # append resname => base[.ins].ext
    # to chipster-outputs.tsv
    write(c(resname,
            if (is.null(ins))
	        paste(base, ext, sep = ".")
	    else
	        paste(base, ins, ext, sep = ".")),
          file = "chipster-outputs.tsv",
          sep = '\t',
          ncolumns = 2,
	  append = TRUE)
}
