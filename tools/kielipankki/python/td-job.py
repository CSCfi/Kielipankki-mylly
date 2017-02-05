# TOOL td-job.py: "Turku Dependency Parser for Finnish - Run Job" (Run a prepared parsing job in the batch system. Use the Prepare Job tool to prepare a text.)
# INPUT data.job TYPE GENERIC
# OUTPUT status.log
# OUTPUT OPTIONAL analyses.txt
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_wraps as wraps

wrapname = "data.job"
tag = "Turku Dependency Wrap"

wraps.restore_inputs(wrapname, tag)
names.output("analyses.txt", names.replace("text.txt", ".tsv"))

wraps.process_wrap(wrapname, tag, "./analyses.txt")
