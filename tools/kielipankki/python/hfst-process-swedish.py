# TOOL hfst-process-swedish.py: "HFST Process Swedish" (Tokenizes text and looks up Swedish morphological analyses of tokens. Output format depends on the underlying combination of lookup tool, its options, and lexical transducer.)
# INPUT text.txt TYPE GENERIC
# OUTPUT readings.txt
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [utf8: "UTF-8"] DEFAULT utf8 (Character encoding, UTF-8)
# PARAMETER Version TYPE [v383: "3.8.3", v390: "3.9.0", v3110: "3.11.0"] DEFAULT v383 (HFST Version)
# PARAMETER InputFormat TYPE [raw: "raw"] DEFAULT raw (Input format)
# PARAMETER OutputFormat TYPE [xerox: "Xerox format", cg: "Constraint Grammar format", apertium: "Apertium format"] DEFAULT xerox (Output format)
# IMAGE comp-16.04-mylly
# RUNTIME python3

import os
import sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_pipeline import hfst_process
from lib_errorlog import consolidate

def process_3_8_3(of):
    home = "/homeappl/appl_taito/ling/hfst/3.8.3"
    processor  = os.path.join(home, "bin", "hfst-proc")
    transducer = os.path.join(home, "share/hfst/sv", "sv-analysis.hfst.ol")

    of = dict(xerox = '--xerox', cg = '--cg', apertium = '--apertium')[of]

    hfst_process(processor, of, '--raw', transducer)

def process_3_9_0(of):
    home = "/homeappl/appl_taito/ling/hfst/3.9.0"
    processor  = os.path.join(home, "bin", "hfst-proc")
    transducer = os.path.join(home, "share/hfst/sv", "sv-analysis.hfst.ol")

    of = dict(xerox = '--xerox', cg = '--cg', apertium = '--apertium')[of]

    hfst_process(processor, of, '--raw', transducer)

def process_3_11_0(of):
    home = "/homeappl/appl_taito/ling/hfst/3.11.0"
    processor  = os.path.join(home, "bin", "hfst-proc")
    transducer = os.path.join(home, "share/hfst/sv", "sv-analysis.hfst.ol")

    of = dict(xerox = '--xerox', cg = '--cg', apertium = '--apertium')[of]

    hfst_process(processor, of, '--raw', transducer)

dict(v383 = process_3_8_3,
     v390 = process_3_9_0,
     v3110 = process_3_11_0)[Version](OutputFormat)

consolidate()
