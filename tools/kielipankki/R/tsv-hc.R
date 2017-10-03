# TOOL tsv-hc.R: "Hierarchical clustering"
# (Cuts item clusters by cosine of attribute counts. Makes dendrogram.)
# INPUT data.tsv: "Data TSV of item, attribute, (count)" TYPE GENERIC
# OUTPUT hc.tsv
# OUTPUT hc.pdf
# OUTPUT hc.png
# OUTPUT hc.svg
# PARAMETER item: "Item field" TYPE COLUMN_SEL
# PARAMETER attr: "Attribute field" TYPE COLUMN_SEL
# PARAMETER freq: "Optional count field" TYPE COLUMN_SEL
# PARAMETER groups: "Number of clusters to cut"
# TYPE INTEGER FROM 1 TO 10 DEFAULT 3
# (Number of clusters to cut, not greater than the number of items.)
# PARAMETER depth: "Dendrogram depth (inches)"
# TYPE INTEGER FROM 3 TO 21 DEFAULT 4
# (Depth of dendrogram graphics in inches, not including item labels.)

# Dendrogram depth is horizontal width, min 3 inches for a nice scale.
# Some vertical space above and below dendrogram remains mysterious
# (with many items, there is too much, with few items, too little).

# TODO to use lib_names.R, already sourced in anticipation
# TODO error out if item == "kMhc"

# TODO error out if cannot make so many groups
# or just make maximal number of groups then
# because cutree will error and not be pretty

# chipster.module.path <- "../.." # testing off-Chipster!
#
# item <- "title"
# attr <- "lemma"
# freq <- "" # "cMcount" # empty when hc.tsv is not counted!
#
# groups <- 4
# 
# depth <- 3

source(paste(chipster.module.path, "R", "lib_names.R",  sep = "/"))
source(paste(chipster.module.path, "R", "lib_ratsv.R",  sep = "/"))

cosine <- function (M) {
    S <- rowSums(M^2)
    (M %*% t(M)) / sqrt(S %*% t(S))
}

# suppose the override of freq field type is harmless if freq == ""
# yes, looks like setNames just *ignores* "" as a name, because of
# course it does? it's ok -- when in R, do as R does -- right?

data <- read.ra.tsv("data.tsv", setNames(list("integer"), freq))

trix <- if (freq == "") { # what a language
            table(data[[item]], data[[attr]], dnn = c(item, attr))
	} else
            xtabs(substitute(foo ~ bar + baz,
                             list(foo = as.name(freq),
                                  bar = as.name(item),
                                  baz = as.name(attr))),
                  data = data)

# trix[1:2,]

# 0 <= cosine <= 1 when in positive quadrant (counts!)
hc <- hclust(as.dist(1 - cosine(trix)))

ks <- cutree(hc, k = groups)

res <- setNames(data.frame(unname(ks),
                           names(ks)),
                c("kMhc", item))

write.table(res, file = "hc.tsv",
            quote = FALSE, sep = "\t",
            row.names = FALSE,
	    fileEncoding = "UTF-8")

# consider multiplicative correction to loi instead of + 0.1
# because now long labels leave tight space on right; could
# apparently set a little outer margin (omi) to cut off any
# excess; on the other hand, cannot do anything about gaps
# above and below dendro with a long list of items while
# short lists are tight, because not understanding what.

# Produce PDF. Consider another PDF producer. Consider embedding of
# fonts. Consider all manner of thing. Because PDF is "Portable".

pdf("hc.pdf") # will be overwritten with actual plot
pdfloi <- max(strwidth(rownames(trix), units = "inches"))
dev.off()

pdf("hc.pdf", height = 1 + 0.2 * nrow(trix),
              width = depth + pdfloi + 0.1)
par(mai = c(0.6, 0.1, 0, pdfloi + 0.1))
plot(as.dendrogram(hc), horiz=T)
dev.off()

# Produce PNG. This actually is "Portable", right?

png("hc.png") # will be overwritten with actual plot
pngloi <- max(strwidth(rownames(trix), units = "inches"))
dev.off()

png("hc.png", height = 1 + 0.2 * nrow(trix),
              width = depth + pngloi + 0.1,
	      units = "in", res = 72)
par(mai = c(0.6, 0.1, 0, pngloi + 0.1))
plot(as.dendrogram(hc), horiz=T)
dev.off()

# Produce SVG.

svg("hc.svg", onefile = TRUE) # will be overwritten with actual plot
# svgloi <- max(strwidth(rownames(trix), units = "inches"))
# Fails in Miilu with tons of CRITICAL fail from some Pango.
# So use PDF width instead. Also, sigh.
svgloi <- pdfloi
dev.off()

svg("hc.svg", height = 1 + 0.2 * nrow(trix),
              width = depth + svgloi + 0.1,
	      onefile = TRUE)
par(mai = c(0.6, 0.1, 0, svgloi + 0.1))
plot(as.dendrogram(hc), horiz=T)
dev.off()
