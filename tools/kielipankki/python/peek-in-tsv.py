# TOOL peek-in-tsv.py: "Peek in a TSV and fail" (Error message contains information)

# This is meant to show the field names and sample values in a TSV to
# the user without producing a file, and then exit with a status so
# that the user gets to see it. Spy for now.

import sys
print('TODO: report on TSV field names here',
      file = sys.stderr)

exit(42)
