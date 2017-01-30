# TOOL aasr-recognize-job.py: "Aalto ASR Recognize Job" (Run a wrapped speech recognition job in the batch system. Use Aalto ASR Recognize Wrap to wrap an audio file.)
# INPUT data.wrap TYPE GENERIC
# OUTPUT status.log
# OUTPUT OPTIONAL script.txt
# OUTPUT OPTIONAL script.textgrid
# OUTPUT OPTIONAL script.eaf
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_wrap as lib

lib.process_wrap("Aalto ASR Recognize Wrap",
                 "./script.txt",
                 "./script.textgrid"
                 "./script.eaf")
