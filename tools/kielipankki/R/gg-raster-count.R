# TOOL gg-raster-count.R: "Raster of counts" (Raster graphic aka heatmap of counts of combinations of two variables. Counts are either sums of a variable, if a count variable is selected, or else counts of observed combinations.)
# INPUT data.tsv TYPE GENERIC
# OUTPUT fig.png
# PARAMETER col.var: "Column variable" TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER row.var: "Row variable" TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER res.var: "Count variable" TYPE COLUMN_SEL DEFAULT EMPTY
# PARAMETER grad.pal: "Gradient palette" TYPE [
#     grey.to.red: "grey to red",
#     grey.to.black: "grey to black",
#     black.to.grey: "black to grey",
#     blues: "light blue to dark blue",
#     yellow.to.red: "yellow to red"
# ] DEFAULT blues
# PARAMETER grad.tra: "Gradient transformation" TYPE [
#    identity: "identity",
#    log10: "log10",
#    log2: "log2",
#    sqrt: "sqrt"
# ] DEFAULT identity
# PARAMETER fig.wd: "Figure width (millimeters)" TYPE INTEGER FROM 40 TO 2000 DEFAULT 160
# PARAMETER fig.ht: "Figure height (millimeters)" TYPE INTEGER FROM 40 TO 2000 DEFAULT 160
# PARAMETER fig.rs: "Figure resolution" TYPE [
#    72: "72 ppi",
#    300: "300 ppi",
#    600: "600 ppi"
# ] DEFAULT 72

if (res.var == "EMPTY") res.var <- ""

library(ggplot2)
library(dplyr)

source(paste(chipster.module.path, "R", "lib_names2.R", sep = "/"))
source(paste(chipster.module.path, "R", "lib_ratsv.R", sep = "/"))

name("fig.png", base("data.tsv", "*.rel.tsv"),
     ins = "raster",
     ext = "png")

data <- read.ra.tsv("data.tsv", setNames(list("integer"), res.var))

# Getting 15 warnings now.

# So calling structure(NULL, class = "waiver") is deprecated but who
# is calling structure(NULL, class = "waiver") and why? (Miilu, new R,
# possibly old ggplot2, is that the reason? - plot looks all right)
# TODO to work it out

col.var <- as.name(col.var)
row.var <- as.name(row.var)

# new.var is other than col.var and row.var
new.var <- as.name(paste0(col.var, row.var))

if (res.var == "") {
    response <- "(count)"
    data <- summarize(group_by(data, !!col.var, !!row.var),
                      !!new.var := n())
} else {
    response <- res.var
    res.var <- as.name(res.var)
    data <- summarize(group_by(data, !!col.var, !!row.var),
                      !!new.var := sum(!!res.var))
}

if (grad.pal == "grey.to.red") {
   lo.col <- "grey"
   hi.col <- "red"
} else if (grad.pal == "grey.to.black") {
   lo.col <- "grey"
   hi.col <- "black"
} else if (grad.pal == "black.to.grey") {
   lo.col <- "black"
   hi.col <- "grey"
} else if (grad.pal == "blues") {
   # ggplot2 defaults
   lo.col <- "#132B43"
   hi.col <- "#56B1F7"
} else if (grad.pal == "yellow.to.red") {
   lo.col <- "yellow"
   hi.col <- "red"
} else {
   stop("this cannot happen")
}

p <- ggplot(data) +
     geom_raster() +
     aes_(x = col.var, y = row.var, fill = new.var) +
     scale_fill_gradient(low = lo.col, high = hi.col, trans = grad.tra) +
     labs(fill = response)

png("fig.tmp",
    width = fig.wd,
    height = fig.ht,
    units = "mm",
    res = as.integer(fig.rs))
print(p)
dev.off()

file.rename("fig.tmp", "fig.png")
