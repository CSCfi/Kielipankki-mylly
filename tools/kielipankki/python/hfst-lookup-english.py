# TOOL hfst-lookup-english.py: "HFST Lookup English" (Looks up English morphological analyses of tokens, each in the first field of a line. Output format depends on the underlying combination of lookup tool, its options, and lexical transducer.)
# INPUT tokens.tsv TYPE GENERIC
# OUTPUT readings.txt
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [utf8: "UTF-8"] DEFAULT utf8 (Character encoding, UTF-8)
# PARAMETER Version TYPE [v383: "3.8.3", v390: "3.9.0"] DEFAULT v383 (HFST Version)
# RUNTIME python3

# Own library in .../common/python3 should be found on sys.path.

import os
from pipeline import hfst_lookup
from errorlog import consolidate

def lookup_3_8_3():
    home = "/homeappl/appl_taito/ling/hfst/3.8.3"
    processor  = os.path.join(home, "bin", "hfst-optimized-lookup")
    transducer = os.path.join(home, "share/hfst/en", "en-analysis.hfst.ol")

    hfst_lookup(processor, transducer)

def lookup_3_9_0():
    home = "/homeappl/appl_taito/ling/hfst/3.9.0"
    processor  = os.path.join(home, "bin", "hfst-optimized-lookup")
    transducer = os.path.join(home, "share/hfst/en", "en-analysis.hfst.ol")

    hfst_lookup(processor, transducer)

dict(v383 = lookup_3_8_3, v390 = lookup_3_9_0)[Version]()

consolidate()
