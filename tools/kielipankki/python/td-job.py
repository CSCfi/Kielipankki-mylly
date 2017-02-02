# TOOL td-job.py: "Turku Dependency Parser for Finnish - Run Job" (Run a wrapped parsing job in the batch system. Use the Prepare Job tool to wrap a text.)
# INPUT data.wrap TYPE GENERIC
# OUTPUT status.log
# OUTPUT OPTIONAL analyses.txt
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_wrap as lib

lib.process_wrap("Turku Dependency Wrap", "./analyses.txt")
