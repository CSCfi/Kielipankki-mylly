# TOOL fiat-finnish-a.py: "Finnish analysis" (Makes a Finnish analysis transducer appear)
# OUTPUT fi-analysis.hfst
# PARAMETER Version TYPE [v_3_12_1: "3.12.1", v_3_11_0: "3.11.0", v_3_9_0: "3.9.0", v_3_8_3: "3.8.3"] DEFAULT v_3_12_1 (HFST Version)
# IMAGE comp-16.04-mylly
# RUNTIME python3

them = dict(v_3_8_3 = '/homeappl/appl_taito/ling/hfst/3.8.3/share/hfst/fi/fi-analysis.hfst.ol',
            v_3_9_0 = '/homeappl/appl_taito/ling/hfst/3.9.0/share/hfst/fi/fi-analysis.hfst.ol',
            v_3_11_0 = '/homeappl/appl_taito/ling/hfst/3.11.0/share/hfst/fi/fi-analysis.hfst.ol',
            v_3_12_1 = '/homeappl/appl_taito/ling/hfst/3.12.1/share/hfst/fi/fi-analysis.hfst.ol')

import os, shutil

# yes, symlink seems fine
os.symlink(them[Version], 'fi-analysis.hfst')
