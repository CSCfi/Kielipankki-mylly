# TOOL aaltoasr-recognize.py: "Aalto ASR - recognize speech from an audio file" (todo)
# INPUT audio TYPE GENERIC
# OUTPUT transcript.txt
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [utf8: "UTF-8"] DEFAULT utf8 (Character encoding, UTF-8)
# PARAMETER Version TYPE [v1: "1.0"] DEFAULT v1 (Tool version)
# PARAMETER InputFormat TYPE [raw: "raw"] DEFAULT raw (Input format todo)
# PARAMETER OutputFormat TYPE [xxx: "xxx"] DEFAULT xxx (Output format todo)

import os
from library.pipeline import aaltoasr_recognize
from library.errorlog import consolidate

def recognize():
    command = [ 'aaltoasr-rec',
                # '--output', 'transcript.txt',
                'audio' ]
    aaltoasr_recognize(command)

consolidate()
