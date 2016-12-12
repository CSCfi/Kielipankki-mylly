# TOOL demotraces.py: "Trace Tokens" (Writes token per line, with positions over the word and over all tokens. Finds token in first field.)
# INPUT tokens.tsv TYPE GENERIC
# OUTPUT traces.txt (Token per line, with position within word)
# OUTPUT traces.tsv (Token per line, with position within word)
# OUTPUT OPTIONAL error.log
# PARAMETER encoding TYPE [utf8: "UTF-8", latin1: "ISO-8859-1"] DEFAULT utf8
# RUNTIME python3

# Since Kielipankki Chipster failed to show a tokens.tsv as
# spreadsheet, with an exception instead, it's better to duplicate the
# result as both traces.txt and traces.tsv for the time being.

# Token tracer to go with the simple tokenizer for the demo.

# On exception, log backtrace and re-raise.

from collections import Counter
import traceback

# encoding = 'UTF-8' # This variable comes from Chipster.

try:
    counter = Counter()
    with open('tokens.tsv', mode = 'rt', encoding = encoding) as records, \
         open('traces.txt', mode = 'wt', encoding = encoding) as traces, \
         open('traces.tsv', mode = 'wt', encoding = encoding) as tracez:

        for k, token in enumerate(( rec.split('\t')[0].strip('\n')
                                    for rec in records ),
                                  start = 1):
            counter[token] += 1
            f = counter[token]
            print(token, f, k, sep = '\t', file = traces)
            print(token, f, k, sep = '\t', file = tracez)

except Exception:
    # Log current exception in error.txt and re-raise
    with open('error.log', mode = 'wt', encoding = 'UTF-8') as errors:
        traceback.print_exc(file = errors)
    raise
