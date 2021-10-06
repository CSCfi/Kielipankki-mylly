# TOOL demotokens.py: "Simply Tokenize Plain Text" (Writes one token per line, with line and token number)
# INPUT text.txt TYPE GENERIC
# OUTPUT tokens.txt (Token per line, with line and token number)
# OUTPUT tokens.tsv (Token per line, with line and token number)
# OUTPUT OPTIONAL error.txt
# PARAMETER encoding TYPE [utf8: "UTF-8", latin1: "ISO-8859-1"] DEFAULT utf8
# IMAGE comp-16.04-mylly
# RUNTIME python3

# Kielipankki Chipster offered to show a tokens.tsv result as
# spreadsheet but got an exception instead. Better to name the result
# tokens.txt until this works - yes, reported it. (Or produce both
# results!  Do that!)

# Simple tokenizer to demonstrate the possibilities.
# Extracts maximal strings of "word characters" as tokens.
# Outputs each "token" on its own line, with line number and token number.
# Output fields are tab-separated.

# On exception, save trace and re-raise.

from itertools import count
import re, traceback

# encoding = 'UTF-8' # This variable comes from Chipster.

try:
    tokenpattern = re.compile(r'\w+')

    with open('text.txt', mode = 'rt', encoding = encoding) as lines, \
         open('tokens.txt', mode = 'wt', encoding = encoding) as tokens, \
         open('tokens.tsv', mode = 'wt', encoding = encoding) as tokenz:
        number = count(start = 1)
        for k, line in enumerate(lines, start = 1):
            for token in tokenpattern.findall(line):
                n = next(number)
                print(token, k, n, sep = '\t', file = tokens)
                print(token, k, n, sep = '\t', file = tokenz)

except Exception:
    # Log current exception in error.txt and re-raise
    with open('error.txt', mode = 'wt', encoding = 'UTF-8') as errors:
        traceback.print_exc(file = errors)
    raise
