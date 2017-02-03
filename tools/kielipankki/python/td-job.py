# TOOL td-job.py: "Turku Dependency Parser for Finnish - Run Job" (Run a wrapped parsing job in the batch system. Use the Prepare Job tool to wrap a text.)
# INPUT data.wrap TYPE GENERIC
# OUTPUT status.log
# OUTPUT OPTIONAL analyses.txt
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names import output, extend
import lib_wrap as lib

# TODO: get the wrapped chipster_inputs.tsv from work directory, base
# chipster_outputs.tsv on that; need to adapt lib to support this.

lib.restore_inputs("./data.wrap")
output("analyses.txt", extend("text.txt", ".tsv"))

lib.process_wrap("Turku Dependency Wrap", "./analyses.txt")
