# TOOL hfst-process2-english.py: "HFST Process2 English" (An alternative processor that tokenizes text using an English morphological analyser. Output format depends on the underlying combination of lookup tool, its options, and lexical transducer.)
# INPUT text.txt TYPE GENERIC
# OUTPUT segments.txt
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [utf8: "UTF-8"] DEFAULT utf8 (Character encoding, UTF-8)
# PARAMETER Version TYPE [v383: "3.8.3", v390: "3.9.0", v3110: "3.11.0"] DEFAULT v383 (HFST Version)
# PARAMETER LineInput TYPE [yes: "yes", no: "no"] DEFAULT no (Whether each line is an input unit. Default separator is an empty line.)
# PARAMETER PrintAll TYPE [yes: "yes", no: "no"] DEFAULT no (Whether to print nonmatching text, whatever that is. Default not.)
# PARAMETER PrintWeight TYPE [yes: "yes", no: "no"] DEFAULT no (Whether to print weights. Default not.)
# PARAMETER OutputFormat TYPE [xerox: "Xerox format", cg: "Constraint Grammar format", segment: "Segment (tokenize)", finnpos: "FinnPos output"] DEFAULT segment (Output format)
# RUNTIME python3

import os
import sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_pipeline import hfst_process2
from lib_errorlog import consolidate

def process_3_8_3():
    home = "/homeappl/appl_taito/ling/hfst/3.8.3"
    processor  = os.path.join(home, "bin", "hfst-proc2")
    transducer = os.path.join(home, "share/hfst/en", "en-analysis.hfst.ol")

    of = dict(xerox = '--xerox',
              cg = '--cg',
              segment = '--segment',
              finnpos = '--finnpos')[OutputFormat]

    command = [processor, of]
    if LineInput == "yes": command.append('--newline')
    if PrintAll == "yes": command.append('--print-all')
    if PrintWeight == "yes": command.append('--print-weight')
    command.append(transducer)

    hfst_process2(*command)

def process_3_9_0(of):
    home = "/homeappl/appl_taito/ling/hfst/3.9.0"
    processor  = os.path.join(home, "bin", "hfst-proc2")
    transducer = os.path.join(home, "share/hfst/en", "en-analysis.hfst.ol")

    of = dict(xerox = '--xerox',
              cg = '--cg',
              segment = '--segment',
              finnpos = '--finnpos')[OutputFormat]

    command = [processor, of]
    if LineInput == "yes": command.append('--newline')
    if PrintAll == "yes": command.append('--print-all')
    if PrintWeight == "yes": command.append('--print-weight')
    command.append(transducer)

    hfst_process2(*command)

def process_3_11_0(of):
    home = "/homeappl/appl_taito/ling/hfst/3.11.0"
    processor  = os.path.join(home, "bin", "hfst-proc2")
    transducer = os.path.join(home, "share/hfst/en", "en-analysis.hfst.ol")

    of = dict(xerox = '--xerox',
              cg = '--cg',
              segment = '--segment',
              finnpos = '--finnpos')[OutputFormat]

    command = [processor, of]
    if LineInput == "yes": command.append('--newline')
    if PrintAll == "yes": command.append('--print-all')
    if PrintWeight == "yes": command.append('--print-weight')
    command.append(transducer)

    hfst_process2(*command)

dict(v383 = process_3_8_3,
     v390 = process_3_9_0,
     v3110 = process_3_11_0)[Version]()

consolidate()
