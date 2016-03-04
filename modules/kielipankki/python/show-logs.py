# TOOL show-logs.py: "Show logs (PREPRODUCTION ONLY)) 
# OUTPUT chipster.log  
# OUTPUT jobs.log
# OUTPUT error.log
# OUTPUT messages.log
# OUTPUT status.log

import shutil

shutil.copyfile('~/chipster/comp/logs/*', '.')

