# TOOL aaltoasr-recognize.py: "Aalto ASR - recognize speech from an audio file" (todo)
# INPUT audio.data TYPE GENERIC
# OUTPUT script.txt
# OUTPUT script.textgrid
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [utf8: "UTF-8"] DEFAULT utf8 (Character encoding, UTF-8 -- of what? todo)
# PARAMETER Version TYPE [v1: "1.0"] DEFAULT v1 (Tool version)
# PARAMETER RawTranscript TYPE [yes: "yes", no: "no"] DEFAULT no (Raw transcript format -- default is to postprocess)
# PARAMETER Script TYPE [yes: "yes"] DEFAULT yes (Always output transcript in aligned.txt)
# PARAMETER SegWord TYPE [yes: "yes"] DEFAULT yes (Always output word level segmentation)
# PARAMETER SegMorph TYPE [yes: "yes", no: "no"] DEFAULT no (Optionally output morph level segmentation)
# PARAMETER SegPhone TYPE [yes: "yes", no: "no"] DEFAULT no (Optionally output phone level segmentation)
# RUNTIME python3

import os
from pipeline import aaltoasr
from errorlog import consolidate

def recognize_1_0():
    home = '/homeappl/appl_taito/ling/aaltoasr/1.0'

    mode = [ 'trans', 'segword' ]
    if SegMorph == 'yes': mode.append('segmorph')
    if SegPhone == 'yes': mode.append('segphone')
    mode = ','.join(mode)

    command = [ 'python3',
                os.path.join(home, 'scripts/aaltoasr-rec'),
                '--output', 'script.txt',
                '--tg', 'script.textgrid',
                '--mode', mode ]
    if RawTranscript == 'yes': command.append('--raw')
    command.append('audio.data')

    aaltoasr(command)

recognize_1_0()

consolidate()
