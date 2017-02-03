# TOOL co.py: "Copy" (Makes a copy. May make another copy!)
# INPUT first.in TYPE GENERIC (First file)
# INPUT OPTIONAL second.in TYPE GENERIC (Second file)
# OUTPUT first.out
# OUTPUT OPTIONAL second.out
# RUNTIME python3

# Optional input is no good? Needs investigation.

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names import output, insert

output("first.out", insert("first.in", "-copy"))
output("second.out", insert("second.in", "-copy"))

import os, shutil
shutil.copy("first.in", "first.out")
if os.path.exists("second.in"):
    shutil.copy("second.in", "second.out")
