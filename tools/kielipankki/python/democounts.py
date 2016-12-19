# TOOL democounts.py: "Count Tokens" (Writes word per line, with decreasing token count. Finds token in first field.)
# INPUT tokens.tsv TYPE GENERIC
# OUTPUT counts.txt (Word per line, with decreasing token count)
# OUTPUT counts.tsv (Word per line, with decreasing token count)
# OUTPUT countsummary.txt (Summary information on token counts)
# OUTPUT OPTIONAL error.txt
# PARAMETER encoding TYPE [utf8: "UTF-8", latin1: "ISO-8859-1"] DEFAULT utf8
# RUNTIME python3

# Since Kielipankki Chipster failed to show a tokens.tsv as
# spreadsheet, with an exception instead, it's better to duplicate the
# result as both counts.txt and counts.tsv for the time being.

# Token counter to go with the simple tokenizer for the demo.

# On exception, save trace and re-raise.

from collections import Counter
import traceback

# encoding = 'UTF-8' # This variable comes from Chipster.

try:

    # Count
    with open('tokens.tsv', mode = 'rt', encoding = encoding) as records:
        counter = Counter(rec.split('\t')[0].strip('\n') for rec in records)

    # Save
    with open('counts.txt', mode = 'wt', encoding = encoding) as counts, \
         open('counts.tsv', mode = 'wt', encoding = encoding) as countz:
        for word, f in counter.most_common():
            print(word, f, sep = '\t', file = counts)
            print(word, f, sep = '\t', file = countz)

    # Summarize
    with open('countsummary.txt', mode = 'wt', encoding = encoding) as summary:

        # Insert some statistics, like 5/11 summaries TODO

        print('The {} most common words with their token counts:'
              .format(10),
              file = summary)
        for word, f in counter.most_common(10):
            print(word, f, sep = '\t', file = summary)

except Exception:
    # Log current exception in error.txt and re-raise
    with open('error.txt', mode = 'wt', encoding = 'UTF-8') as errors:
        traceback.print_exc(file = errors)
    raise
