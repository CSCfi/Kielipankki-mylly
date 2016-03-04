# TOOL finnish-analyze.py: "Restart comp on Taito" 

import subprocess
import os
from time import sleep

my_cmd='cd ~/git/Kielipankki-Chipster/ && git pull'

p = subprocess.Popen(my_cmd, shell=True)
os.waitpid(p.pid, 0)


my_cmd='~/chipster/comp/bin/chipster-comp stop'

p = subprocess.Popen(my_cmd, shell=True)
os.waitpid(p.pid, 0)

sleep(1)

my_cmd='~/chipster/comp/bin/chipster-comp start'

p = subprocess.Popen(my_cmd, shell=True)
os.waitpid(p.pid, 0)
