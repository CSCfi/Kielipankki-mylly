# TOOL kp-test-data-in-out.py: "Test data input and output in Python" (Data input output test.) 
# INPUT input.txt TYPE GENERIC
# OUTPUT output.txt

import shutil

shutil.copyfile('input.txt', 'output.txt')

# test update
