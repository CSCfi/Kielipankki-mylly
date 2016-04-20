# TOOL aaltoasr-align.py: "Aalto ASR - align a transcription to a speech audio file" (todo)
# INPUT audio.data TYPE GENERIC
# INPUT script.txt TYPE GENERIC
# OUTPUT aligned.txt
# OUTPUT aligned.textgrid
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [utf8: "UTF-8"] DEFAULT utf8 (Character encoding, UTF-8 -- of what? TODO)
# PARAMETER Version TYPE [v1: "1.0"] DEFAULT v1 (Aalto ASR version)
# PARAMETER SegWord TYPE [yes: "yes"] DEFAULT yes (Always output word level segmentation)
# PARAMETER SegPhone TYPE [yes: "yes", no: "no"] DEFAULT no (Optionally output phone level segmentation)

import os
from library.pipeline import aaltoasr_align
from library.errorlog import consolidate

def align_1_0():
    home = '/homeappl/appl_taito/ling/aaltoasr/1.0'
    mode = ( 'segword' if SegPhone == 'no' else 'segword,segphone' )
    command = [ 'python3',
                os.path.join(home, 'scripts/aaltoasr-align'),
                '--output', 'aligned.txt',
                '--tg', 'aligned.textgrid',
                '--trans', 'script.txt',
                '--mode', mode,
                'audio.data'
    ]
    aaltoasr(command)

align_1_0()

consolidate()
