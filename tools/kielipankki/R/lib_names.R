# Source this in a Mylly tool script and then rename outputs
# based on inputs like in this example:
#
# out.map("graph.any", replace.suffix("data.tsv", ".pdf"))
# - user sees input file "data.tsv" as "foo.tsv", say
# - script sees input file as "data.tsv"
# - script creates output file "graph.any"
# - uses sees output file as "foo.pdf" (input name with new suffix)

library(tools) # for file_path_sans_ext, file_ext

external_name <- function (internal) {
    inputs <- read.table("chipster-inputs.tsv", colClasses = "character")
    external <- inputs[inputs$V1 == internal,]$V2

    if (length(external) == 1) {
        external
    } else {
    
        # this should not happen, so only the developer should
	# ever see this error message
	
        stop("internal name ", internal,
	     " is not mapped to a unique external name")
    }
}

check_extension <- function (internal, extensions) {

    # use this to inform the user that they are (probably) applying
    # the tool to a wrong file (usually by mistake)

    external <- external_name(internal)
    if (any(endsWith(external, extensions))) {
    } else {
        stop("\nname ", external, " does not end with ",
	     paste(extensions, collapse = " or "))
    }
}

out.map <- function(paraname, username) {
    # append paraname TAB username NL to chipster-outputs.tsv
    write(c(paraname, username), "chipster-outputs.tsv",
          sep = '\t',
          ncolumns = 2,
	  append = TRUE)
}

sensible.extensions <- c("csv", "html",
                         "jpg", "json", "png", "pdf", "svg",
                         "tsv", "txt", "xhtml", "xml")

replace.suffix <- function(paraname, suffix) {
    # read original dataname at facename in chipster-inputs.tsv
    # replace its suffix
    username <- external_name(paraname)    
    sansname <- file_path_sans_ext(username)
    ext <- file_ext(username)
    if (any(sensible.extensions == ext)) {
        res <- paste0(sansname, suffix, collapse = "")
    } else {
        res <- paste0(username, suffix, collapse = "")
    }
}

# testing, requires image{1,2}.jpg in chipster_inputs.tsv
# out.map("graph.any", replace.suffix("image1.jpg", ".pdf"))
# out.map("graph.ics", replace.suffix("image2.jpg", ".pdf"))
