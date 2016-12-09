# TOOL english-analyze.py: "english-analyze.sh on Taito" 
# INPUT input TYPE GENERIC
# OUTPUT output


import subprocess
import os

my_cmd='iconv -f cp1252 -t utf-8 input|english-analyze.sh |iconv -futf-8 -tcp1252 > output'

p = subprocess.Popen(my_cmd, shell=True)
os.waitpid(p.pid, 0)

