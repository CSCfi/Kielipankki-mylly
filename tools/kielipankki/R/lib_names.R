# source this and then have a tool do these:
# out.map("graph.any", suf.fix("data.tsv", ".pdf"))

library(tools) # for file_path_sans_ext, file_ext

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

suf.fix <- function(paraname, suffix) {
    # read original dataname at facename in chipster-inputs.tsv
    # replace its suffix
    inputs <- read.table("chipster-inputs.tsv", colClasses = "character")
    #print(inputs)
    username <- inputs[inputs$V1 == paraname,]$V2

    # crash here if username is not a filename (but is empty)
    if (length(username) == 1) {} else crash
    
    sansname <- file_path_sans_ext(username)
    ext <- file_ext(username)
    if (any(sensible.extensions == ext)) {
        res <- paste0(sansname, suffix, collapse = "")
    } else {
        res <- paste0(username, suffix, collapse = "")
    }
}

# testing, requires image{1,2}.jpg in chipster_inputs.tsv
# out.map("graph.any", suf.fix("image1.jpg", ".pdf"))
# out.map("graph.ics", suf.fix("image2.jpg", ".pdf"))
