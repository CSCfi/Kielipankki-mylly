# TOOL powerplot.R: "Power Law Plot of Token Counts" (Plots numbers of words with observed frequencies. Input should have each word in UTF-8 and its frequency on a line, separated by a tab.)
# INPUT counts.tsv TYPE GENERIC
# OUTPUT power.pdf
# OUTPUT power.png
# OUTPUT power.svg
# OUTPUT OPTIONAL error.log

# Desired plot types could be parameters.
# Now makes all of pdf, png, svg.
# Need to learn what works best.

makeplot <- function (data) {
   par(xlog = TRUE, ylog = TRUE)
   plot(data,
        xlab = "Occurrences", 
        ylab = "Words",
       	type = "p")
}

makepdf <- function (data) {
   pdf(file = "power.pdf")
   makeplot(data)
   dev.off()
}

makepng <- function (data) {
   png(file = "power.png")
   makeplot(data)
   dev.off()
}

makesvg <- function (data) {
   svg(file = "power.svg")
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

# The actual computation happens here in table(table(data)).
data <- tryCatch(table(table(data)),
                 error = function (e) fail("tabulating data"))

tryCatch(makepdf(data),
         error = function (e) fail("making pdf"))

tryCatch(makepng(data),
         error = function (e) fail("making png"))

tryCatch(makesvg(data),
         error = function (e) fail("making svg"))
