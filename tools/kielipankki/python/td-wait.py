# TOOL td-wait.py: "Turku Dependency Parser for Finnish - Wait for Results" (Waits for the results of a parsing job in the batch system. The input file is the job file from the corresponding submit tool.)
# INPUT generic.job TYPE GENERIC
# OUTPUT analyses.txt
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import os
import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_jobs as jobs

job = "generic.job"
tag = "Turku Dependency Job"

jobs.restore_inputs(job, tag)
names.output("analyses.txt", names.replace("text.txt", ".tsv"))

jobs.wait(job, tag, "analyses.txt")
