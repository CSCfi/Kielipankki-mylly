# TOOL hfst-lookup-finnish.py: "HFST Lookup Finnish" (Looks up Finnish morphological analyses of tokens, each in the first field of a line. Output format depends on the underlying combination of the lookup tool, its options, and the lexical transducer.)
# INPUT tokens.tsv TYPE GENERIC
# OUTPUT readings.txt
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [utf8: "UTF-8"] DEFAULT utf8 (Character encoding, UTF-8)
# PARAMETER Version TYPE [v383: "3.8.3", v390: "3.9.0"] DEFAULT v383 (HFST Version)

import os
import sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_pipeline import hfst_lookup
from lib_errorlog import consolidate

def lookup_3_15_0():
    home = "/appl/ling/hfst/3.15.0"
    processor  = os.path.join(home, "bin", "hfst-optimized-lookup")
    transducer = os.path.join(home, "share/hfst/fi", "fi-analysis.hfst.ol")

    hfst_lookup(processor, transducer)

def lookup_3_9_0():
    home = "/homeappl/appl_taito/ling/hfst/3.9.0"
    processor  = os.path.join(home, "bin", "hfst-optimized-lookup")
    transducer = os.path.join(home, "share/hfst/fi", "fi-analysis.hfst.ol")

    hfst_lookup(processor, transducer)

dict(v383 = lookup_3_15_0, v390 = lookup_3_9_0)[Version]()

consolidate()
