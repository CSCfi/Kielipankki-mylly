# TOOL demotokens.py: "Simply Tokenize Plain Text" (Writes one token per line, with line and token number)
# INPUT text.txt TYPE GENERIC
# OUTPUT tokens.tsv (Token per line, with line and token number)
# OUTPUT OPTIONAL error.txt
# PARAMETER encoding TYPE [utf8: "UTF-8", latin1: "ISO-8859-1"] DEFAULT utf8

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
         open('tokens.txt', mode = 'wt', encoding = encoding) as tokens:
        number = count(start = 1)
        for k, line in enumerate(lines, start = 1):
            for token in tokenpattern.findall(line):
                print(token, k, next(number), sep = '\t', file = tokens)

except Exception:
    # Log current exception in error.txt and re-raise
    with open('error.txt', mode = 'wt', encoding = 'UTF-8') as errors:
        traceback.print_exc(file = errors)
    raise
