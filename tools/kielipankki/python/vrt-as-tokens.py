# TOOL vrt-as-tokens.py: "Extract tokens from VRT" (Extract token sequences from a VRT document, with token per line and an empty line after each sentences-like unit. Empty input lines are ignored. Markup element that can occur within sentence need to be named as parameters.)
# INPUT input.vrt TYPE GENERIC
# OUTPUT output.txt
# PARAMETER ign1 TYPE STRING DEFAULT EMPTY
# PARAMETER ign2 TYPE STRING DEFAULT EMPTY
# PARAMETER ign3 TYPE STRING DEFAULT EMPTY
# PARAMETER ign4 TYPE STRING DEFAULT EMPTY
# IMAGE comp-16.04-mylly
# RUNTIME python3

import html, os, sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
from lib_vrt import VeRTicalError, Positionals, screen, hoisted
from lib_vrt import sentences

name('output.txt', base('input.vrt', '*.vrt'),
     ins = 'tokens', ext = 'txt')

# markup element names that must be hoisted out of the way so that
# they do not break token sequences
hoistable = list(ign for ign in (ign1, ign2, ign3, ign4)
                 if ign not in ('EMPTY', ''))

try:
    with open('input.vrt', encoding = 'UTF-8') as source, \
         open('hoisted.tmp', mode = 'w', encoding = 'UTF-8') as out:
        for line in hoisted(screen(source, Positionals()), hoistable):
            print(line, file = out)
except VeRTicalError as exn:
    print(exn, file = sys.stderr)
    exit(1)

with open('hoisted.tmp', encoding = 'UTF-8') as source, \
     open('output.tmp', mode = 'w', encoding = 'UTF-8') as out:
    for sentence in sentences(source):
        print(*map(html.unescape, sentence),
              sep = '\n', end = '\n\n', file = out)

os.rename('output.tmp', 'output.txt')
