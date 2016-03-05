# TOOL rankplot.R: "Decreasing Plot of Token Counts" (Plots observed word frequencies in decreasing order. Input should have each word in UTF-8 and its frequency on a line, separated by a tab.)
# INPUT counts.tsv TYPE GENERIC
# OUTPUT rank.pdf
# OUTPUT rank.png
# OUTPUT rank.svg
# OUTPUT OPTIONAL error.log

# Desired plot types could be parameters.
# Now makes all of pdf, png, svg.
# Need to learn what works best.

makeplot <- function (data) {
   plot(data,
        xlab = "Rank", 
        ylab = "Occurrences",
        log = "xy",
        type = "p")
}

makepdf <- function (data) {
   pdf(file = "rank.pdf")
   makeplot(data)
   dev.off()
}

makepng <- function (data) {
   png(file = "rank.png")
   makeplot(data)
   dev.off()
}

makesvg <- function (data) {
   svg(file = "rank.svg")
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

data <- tryCatch(read.table(file = "counts.tsv",
                            header = FALSE,
                            sep = "\t",
                            quote = "",
                            comment.char = "#",
                            colClasses = c("NULL", "integer"),
                            encoding = "UTF-8"),
                 error = function (e) fail("reading counts.tsv"))

# The actual computation happens here in sort(data[,1], decreasing = TRUE).
data <- tryCatch(sort(data[,1], decreasing = TRUE),
                 error = function (e) fail("ordering data"))

tryCatch(makepdf(data),
         error = function (e) fail("making pdf"))

tryCatch(makepng(data),
         error = function (e) fail("making png"))

tryCatch(makesvg(data),
         error = function (e) fail("making svg"))
