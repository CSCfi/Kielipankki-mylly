# TOOL whereplot.R: "Cumulative Plot of First Occurrences" (Plots the growth of vocabulary along tokens. Input should have each word in UTF-8 and its token trace and another number on a line, separated by tabs.)
# INPUT traces.tsv TYPE GENERIC
# OUTPUT where.pdf
# OUTPUT where.png
# OUTPUT where.svg
# OUTPUT OPTIONAL fail.log
# PARAMETER word1 TYPE STRING DEFAULT "word1"
# PARAMETER word2 TYPE STRING DEFAULT "word2"
# PARAMETER word3 TYPE STRING DEFAULT "word3"
# PARAMETER word4 TYPE STRING DEFAULT "word4"

# These variables, they should come from Chipster.
# But when testing off-line, there is no Chipster.
# word1 <- "a"
# word2 <- "the"
# word3 <- "on"
# word4 <- "and"

# Desired plot types could be parameters.
# Now makes all of pdf, png, svg.
# Need to learn what works best.

makeplot <- function (data) {

   limits <- data$limits
   words <- data$words
   places <- data$places

   plot(c(),
        xlim = limits,
        ylim = c(1, length(words) + .5),
        xlab = "Position",
        ylab = "",
	yaxt = "n") # no such axis

   for (w in 1:length(words)) {
      y = length(words) - w + 1 # because axis is upside down wrt w
      text(1, y, pos = 4, labels = words[w])
      lines(limits, rep(y + .2, 2), lty = "dotted")
      points(places[[w]], rep(y + .2, length(places[[w]])))
   }
}

makepdf <- function (data) {
   pdf(file = "where.pdf")
   makeplot(data)
   dev.off()
}

makepng <- function (data) {
   png(file = "where.png")
   makeplot(data)
   dev.off()
}

makesvg <- function (data) {
   svg(file = "where.svg")
   makeplot(data)
   dev.off()
}

fail <- function (cond, when) {
   cat("Fail plotting places when ", when, ":\n",
       cond$message, "\n\n",
       sep = "",
       file = "fail.log",
       append = TRUE)
   cat(cond$message) # should go to stderr
   cat(cond$call)    # should go to stderr
}

data <- tryCatch(read.table(file = "traces.tsv",
                            header = FALSE,
                            sep = "\t",
                            quote = "",
                            comment.char = "#",
			    col.names = c("Tok", "None", "Loc"),
                            colClasses = c("character", "NULL", "integer"),
                            encoding = "UTF-8"),
                 condition = function (c) fail(c, "reading traces.tsv"))

data <- tryCatch(list(limits = c(1, length(data$Tok)),
                      words = c(word1, word2, word3, word4),
                      places = lapply(c(word1, word2, word3, word4),
                                      function (w) {
                                         data$Loc[data$Tok == w]
                                      })),
                 condition = function (c) fail(c, "locating words"))

tryCatch(makepdf(data),
         condition = function (c) { fail(c, "making pdf") })

tryCatch(makepng(data),
         condition = function (c) fail(c, "making png"))

tryCatch(makesvg(data),
         condition = function (c) fail(c, "making svg"))
