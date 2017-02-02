# TOOL co.py: "Copy" (Makes a copy. May make another copy!)
# INPUT first.in TYPE GENERIC (First file)
# INPUT OPTIONAL second.in TYPE GENERIC (Second file)
# OUTPUT first.out
# OUTPUT OPTIONAL second.out
# RUNTIME python3

import os, shutil
shutil.copy("first.in", "first.out")
if os.path.exists("second.in"):
    shutil.copy("second.in", "second.out")

with open("chipster-inputs.tsv", "r") as ins:
    with open("chipster-outputs.tsv", "w") as outs:
        inputs = dict(rec.strip('\r\n').split('\t')[:2]
                      for rec in ins
                      if not rec.startswith('#'))
        print("first.out", inputs["first.in"], sep = '\t', file = outs)
        print("second.out", inputs["second.in"], sep = '\t', file = outs)
