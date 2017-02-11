# TOOL aasr-recognize-wait.py: "Aalto Speech Recognizer - Wait for Results" (Waits for the results of a speech recognition job in the batch system. The input is the job file from the corresponding submit tool.)
# INPUT generic.job TYPE GENERIC
# OUTPUT script.txt
# OUTPUT script.textgrid
# OUTPUT script.eaf
# OUTPUT OPTIONAL error.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# RUNTIME python3

# Made batch stdout and stderr available in Mylly at least for the
# time being. Need to work out the details.

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names
import lib_jobs as jobs

job = "generic.job"
tag = "Aalto Recognition Job"

jobs.restore_inputs(job, tag)
names.output("script.txt", names.replace("audio.wav", ".txt"))
names.output("script.textgrid", names.replace("audio.wav", ".textgrid"))
names.output("script.eaf", names.replace("audio.wav", ".eaf"))

jobs.process_wrap(job, tag,
                  "script.txt",
                  "script.textgrid",
                  "script.eaf",
                  "stdout.log",
                  "stderr.log")
