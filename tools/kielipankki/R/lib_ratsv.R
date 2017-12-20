read.ra.tsv <- function (filename, types = list()) {

    # read a table enforcing all manner of things
    # and using Mylly prefixes to indicate type,
    # inhibiting all manner of default damage that
    # *might* happen to the data some day;
    # TODO need to deal with missing data some day

    # Override "datami" -> "factor" with "Date" (or any other
    # prefixism) with types = setNames(list("pvm"), "datami") --
    # though as of this writing Mylly does not do dates yet! The point
    # is that types[["datami"]] is then non-NULL but types[["other"]]
    # is NULL and vanishes in c(). This is R. You will be assimilated.
    
    source <- file(filename, encoding = "UTF-8")
    open(source)
    
    fieldnames <- unlist(strsplit(readLines(source, n = 1), split = "\t"))
    fieldtypes <- unname(sapply(fieldnames, function (name) {
        c(types[[name]],
          switch(ra.tsv.prefix(name),
	         cM = "integer",
	         kM = "integer",
	         # other type prefixes here
	         "factor"))[1]
    }))

    data <- read.delim(source,
                       col.names = fieldnames,
                       colClasses = fieldtypes,
                       header = FALSE,
                       quote = "",
		       fill = FALSE)

    close(source) # aw

    data
}

ra.tsv.prefix <- function (fieldname) {

   # return the Mylly prefix of fieldname, if any
   # return an empty string, if not any
   # a Mylly prefix is a sequence of lower case letters followed
   # by an upper case M (which stands for Mylly) indicating type
   
   regmatches(fieldname, regexpr("^([[:lower:]]+M)?", fieldname))
}
