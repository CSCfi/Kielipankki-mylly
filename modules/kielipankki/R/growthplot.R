# TOOL growthplot.R: "Cumulative Plot of First Occurrences" (Plots the growth of vocabulary along tokens. Input should have each word in UTF-8 and its token trace and another number on a line, separated by tabs.)
# INPUT traces.tsv TYPE GENERIC
# OUTPUT growth.pdf
# OUTPUT growth.png
# OUTPUT growth.svg
# OUTPUT OPTIONAL error.log

# Desired plot types could be parameters.
# Now makes all of pdf, png, svg.
# Need to learn what works best.

makeplot <- function (data) {
   plot(data,
        xlab = "Position", 
        ylab = "Vocabulary",
        type = "s")
}

makepdf <- function (data) {
   pdf(file = "growth.pdf")
   makeplot(data)
   dev.off()
}

makepng <- function (data) {
   png(file = "growth.png")
   makeplot(data)
   dev.off()
}

makesvg <- function (data) {
   svg(file = "growth.svg")
   makeplot(data)
   dev.off()
}

fail <- function (when) {
   # Some user-visible logging on errors but not too much.
   # Should also log in stdout/stderr for admins to see.
   cat("Fail ", when, "\n",
       sep = "",
       file = "error.log",
       append = TRUE)
}

data <- tryCatch(read.table(file = "traces.tsv",
                            header = FALSE,
                            sep = "\t",
                            quote = "",
                            comment.char = "#",
                            colClasses = c("NULL", "integer", "NULL"),
                            encoding = "UTF-8"),
                 error = function (e) fail("reading traces.tsv"))

# The actual computation happens here in cumsum(data[,1] == 1).
data <- tryCatch(cumsum(data[,1] == 1),
                 error = function (e) fail("ordering data"))

tryCatch(makepdf(data),
         error = function (e) fail("making pdf"))

tryCatch(makepng(data),
         error = function (e) fail("making png"))

tryCatch(makesvg(data),
         error = function (e) fail("making svg"))
