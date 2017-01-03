# TOOL finnish-analyze.py: "finnish-analyze.sh on Taito" 
# INPUT input TYPE GENERIC
# OUTPUT output.txt
# OUTPUT diagnostics.txt


import subprocess
import os

my_cmd='iconv -f cp1252 -t utf-8 input|finnish-analyze.sh |iconv -futf-8 -tcp1252 > output.txt 2> diagnostics.txt'

p = subprocess.Popen(my_cmd, shell=True)
os.waitpid(p.pid, 0)

