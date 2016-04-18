# TOOL aaltoasr-align.py: "Aalto ASR - align a transcription to a speech audio file" (todo)
# INPUT transcript.txt TYPE GENERIC
# INPUT audio.data TYPE GENERIC
# OUTPUT alignment.txt
# OUTPUT alignment.textgrid
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [utf8: "UTF-8"] DEFAULT utf8 (Character encoding, UTF-8)
# PARAMETER Version TYPE [v1: "1.0"] DEFAULT v1 (Tool version)
# PARAMETER InputFormat TYPE [raw: "raw"] DEFAULT raw (Input format todo)
# PARAMETER OutputFormat TYPE [xxx: "xxx"] DEFAULT xxx (Output format todo)

import os
from library.pipeline import aaltoasr_align
from library.errorlog import consolidate

def recognize():
    command = [ 'python3',
                '/homeappl/appl_taito/ling/aaltoasr/1.0/scripts/aaltoasr-align',
                '--output', 'alignment.txt',
                '--tg', 'alignment.textgrid',
                '--trans', 'transcript.txt',
                'audio.data' ]
    aaltoasr_recognize(command)

recognize()

consolidate()
