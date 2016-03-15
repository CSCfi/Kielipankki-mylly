# TOOL hfst-lookup-finnish.py: "HFST Lookup Finnish" 
# INPUT tokens.tsv TYPE GENERIC
# OUTPUT readings.tsv
# OUTPUT OPTIONAL error.log

# Make HFST _version_ a parameter as soon as the tool is working. Add
# version 3.9.0 at that time. Only then expand to other languages and
# other forms of processing.

import os
from library.pipeline import hfst_lookup
from library.errorlog import consolidate

def lookup_3_8_3():
    home = "/homeappl/appl_taito/ling/hfst/3.8.3"
    processor  = os.path.join(home, "bin", "hfst-optimized-lookup")
    transducer = os.path.join(home, "share/hfst/fi", "fi-analysis.hfst.ol")

    hfst_lookup(processor, transducer)

lookup_3_8_3()

consolidate()
