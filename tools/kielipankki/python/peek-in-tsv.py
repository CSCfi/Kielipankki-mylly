# TOOL peek-in-tsv.py: "Peek in a TSV and fail" (Error message contains information)
# RUNTIME python3

# This is meant to show the field names and sample values in a TSV to
# the user without producing a file, and then exit with a status so
# that the user gets to see it. Spy for now.

import sys
print('chipster_module_path:', repr(chipster_module_path),
      file = sys.stderr)

exit(42)
