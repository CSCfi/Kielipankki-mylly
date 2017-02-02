# TOOL td-parse-finnish.py: "Turku Dependency Parser for Finnish - Run Directly" (Segments Finnish text into sentences and tokens. Annotates each sentence with a morpho-syntactic structure. Runs directly on a server where other people also work.)
# INPUT text.txt TYPE GENERIC
# OUTPUT analyses.txt
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import os
import sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_pipeline import turku_parser_wrapper
from lib_errorlog import consolidate

def parse_text():
    home="/appl/ling/finnish-process/share/hfst/fi/Finnish-dep-parser-alpha"
    turku_parser_wrapper(os.path.join(home, "parser_wrapper.sh"))

parse_text()

consolidate()
