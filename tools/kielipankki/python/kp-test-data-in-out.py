# TOOL kp-test-data-in-out.py: "Test data input and output in Python" (Data input output test.) 
# INPUT input TYPE GENERIC
# OUTPUT output

import shutil
import os

f = open('output', 'w')
f.write("p "+os.getcwd())
f.close()  

#shutil.copyfile('input', 'output')

