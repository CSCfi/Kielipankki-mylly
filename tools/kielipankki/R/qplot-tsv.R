# TOOL qplot-tsv.R: "Visualize two-variable relationship"
# (Graph the relationship of two variables, using qplot of ggplot2 library in R)
# INPUT data.tsv TYPE GENERIC
# OUTPUT graph.any
# PARAMETER vi.file: "file type" TYPE [pdf: "pdf", png: "png", svg: "svg"] DEFAULT png
# PARAMETER vi.plot: "plot type" TYPE [points: "points", jitter: "jitter", boxplot: "boxplot"] DEFAULT points
# PARAMETER vi.x: "x variable" TYPE STRING
# PARAMETER vi.xt TYPE [logical: "logical", integer: "integer", numeric: "numeric", factor: "factor"] DEFAULT integer
# PARAMETER vi.y: "y variable" TYPE STRING
# PARAMETER vi.yt TYPE [logical: "logical", integer: "integer", numeric: "numeric", factor: "factor"] DEFAULT integer
# PARAMETER OPTIONAL vi.colour: "colour grouping variable (factor)" TYPE STRING
# PARAMETER OPTIONAL vi.shape: "shape grouping variable (factor)" TYPE STRING
# PARAMETER OPTIONAL vi.size: "size variable (numeric)" TYPE STRING

# Testing off-chipster (requires and produces files):
# 
# chipster.module.path <- ".."
# 
# vi.file <- "pdf"
# vi.plot <- "points"
# vi.x <- "ref"
# vi.xt <- "integer"
# vi.y <- "dephead"
# vi.yt <- "integer"
# 
# vi.colour <- "Match" # "pos" does it only use one? oh, there be few Match - yes!
# vi.shape <- NULL # "Match"
# vi.size <- "Tok"

source(paste(chipster.module.path, "R", "lib_names.R",  sep = "/"))

check_extension("data.tsv", c(".tsv")) # enforces *.tsv for input file

vi.ext <- switch(vi.file, pdf = ".pdf", png = ".png", svg = ".svg")
out.map("graph.any", replace.suffix("data.tsv", vi.ext))

library("ggplot2")

# intending it to be assumed that the file be UTF-8
# hoping R not to do anything insane instead

vi.from <- file("data.tsv", encoding = "UTF-8")
open(vi.from)

# read column names

vi.head <- unlist(strsplit(readLines(vi.from, n = 1), split = "\t"))

# assign "colClass" names to the relevant column names

vi.core <- c(setNames(as.list(vi.xt), vi.x),
             setNames(as.list(vi.yt), vi.y),
             if (sum(nchar(vi.colour)) == 0) list() else setNames(as.list("factor"), vi.colour),
             if (sum(nchar(vi.shape)) == 0) list() else setNames(as.list("factor"), vi.shape),
             if (sum(nchar(vi.size)) == 0) list() else setNames(as.list("numeric"), vi.size))

if (!all(names(vi.core) %in% vi.head)) {
    print(vi.core)
    print(names(vi.core))
    print(length(names(vi.core)))
    stop("\nAttributes expected to be graphed but not observed in data.",
         "\nExpecting: ", paste(names(vi.core), collapse = " "),
	 "\nObserving: ", paste(vi.head, collapse = " "),
	 "\n", "FALSE in the following should indicate which is missing",
	 "\n", paste(as.character(names(vi.core) %in% vi.head), collapse = " "),
	 "\n")
}

# assign "colClass" names or "NULL" (the string) to all column names
# in their order in the file, then drop the names so that the result
# is usable as colClasses in read.delim

vi.type <- unname(sapply(vi.head, function (name) {
                             core <- vi.core[[name]]
                             if (is.null(core)) "NULL" else core
                         }))

# read relevant columns of data as data.frame, skip other columns

vi.data <- read.delim(vi.from, quote = "",
                      header = FALSE,
                      col.names = vi.head,
                      colClasses = vi.type)
close(vi.from)

vi.dev <- switch(vi.file, pdf = pdf, png = png, svg = svg)

vi.dev(file = "graph.any")
plot <- eval(substitute(qplot(x, y, data = vi.data),
                       list(x = as.name(vi.x),
                            y = as.name(vi.y))))

if (sum(nchar(vi.colour)) > 0) {
    plot <- plot + eval(substitute(aes(colour = variable),
                                   list(variable = as.name(vi.colour))))
}

if (sum(nchar(vi.shape)) > 0) {
    plot <- plot + eval(substitute(aes(shape = variable),
                                   list(variable = as.name(vi.shape))))
}

if (sum(nchar(vi.size)) > 0) {
    plot <- plot + eval(substitute(aes(size = variable),
                                   list(variable = as.name(vi.size))))
}

plot
dev.off()
