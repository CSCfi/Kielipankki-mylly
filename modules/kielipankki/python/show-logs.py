# TOOL show-logs.py: "Show logs (PREPRODUCTION ONLY)" 
# OUTPUT chipster.log  
# OUTPUT jobs.log
# OUTPUT error.log
# OUTPUT messages.log
# OUTPUT status.log

import shutil

shutil.copyfile('/homeappl/home/kp-ruser/chipster/comp/logs/chipster.log', 'chipster.log')
shutil.copyfile('/homeappl/home/kp-ruser/chipster/comp/logs/jobs.log', 'jobs.log')
shutil.copyfile('/homeappl/home/kp-ruser/chipster/comp/logs/error.log', 'error.log')
shutil.copyfile('/homeappl/home/kp-ruser/chipster/comp/logs/messages.log', 'messages.log')
shutil.copyfile('/homeappl/home/kp-ruser/chipster/comp/logs/status.log', 'status.log')

