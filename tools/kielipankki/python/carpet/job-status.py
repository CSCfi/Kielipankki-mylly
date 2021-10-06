# TOOL job-status.py: "Current State" (Get a report on the current state of a Mylly batch job that is still in the batch system.)
# INPUT generic.job TYPE GENERIC
# OUTPUT state.log
# OUTPUT OPTIONAL error.log
# IMAGE comp-16.04-mylly
# RUNTIME python3

import os
import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_jobs as jobs

job = "generic.job"

names.output("state.log", names.replace(job, "-state.log"))

jobs.check(job)
