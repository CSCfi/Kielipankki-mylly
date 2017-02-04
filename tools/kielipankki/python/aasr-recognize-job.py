# TOOL aasr-recognize-job.py: "Aalto ASR Recognize - Run Job" (Run a wrapped speech recognition job in the batch system. Use the corresponding Prepare Job tool to wrap an audio file.)
# INPUT data.wrap TYPE GENERIC
# OUTPUT status.log
# OUTPUT OPTIONAL script.txt
# OUTPUT OPTIONAL script.textgrid
# OUTPUT OPTIONAL script.eaf
# OUTPUT OPTIONAL error.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# RUNTIME python3

# Made batch stdout and stderr available in Mylly at least for the
# time being. Need to work out the details.

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_wrap as wraps
import lib_names as names

tag = "Aalto ASR Recognize Wrap"
wraps.restore_inputs("./data.wrap", tag)
names.output("script.txt", names.replace("audio.wav", ".txt"))
names.output("script.textgrid", names.replace("audio.wav", ".textgrid"))
names.output("script.eaf", names.replace("audio.wav", ".eaf"))

wraps.process_wrap(tag,
                   "script.txt",
                   "script.textgrid",
                   "script.eaf",
                   "stdout.log",
                   "stderr.log")
