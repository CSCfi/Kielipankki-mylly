# TOOL td-job.py: "Turku Dependency Parser for Finnish - Run Job" (Run a wrapped parsing job in the batch system. Use the Prepare Job tool to wrap a text.)
# INPUT data.wrap TYPE GENERIC
# OUTPUT status.log
# OUTPUT OPTIONAL analyses.txt
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_wrap as wraps

# TODO: get the wrapped chipster_inputs.tsv from work directory, base
# chipster_outputs.tsv on that; need to adapt lib to support this.

tag = "Turku Dependency Wrap"
wraps.restore_inputs("./data.wrap", tag)
names.output("analyses.txt", names.replace("text.txt", ".tsv"))

wraps.process_wrap(tag, "./analyses.txt")
