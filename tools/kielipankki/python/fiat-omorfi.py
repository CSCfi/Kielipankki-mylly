# TOOL fiat-omorfi.py: "Let there be Omorfi" (Makes the Omorfi transducer appear, suitable for analysis of Finnish word forms)
# OUTPUT fi-analysis.hfst
# PARAMETER Version TYPE [v3121: "3.12.1", v3110: "3.11.0", v3090: "3.9.0", v3083: "3.8.3"] DEFAULT v3121 (HFST Version)
# RUNTIME python3

them = dict(v3083 = '/homeappl/appl_taito/ling/hfst/3.8.3/share/hfst/fi/fi-analysis.hfst.ol',
            v3090 = '/homeappl/appl_taito/ling/hfst/3.9.0/share/hfst/fi/fi-analysis.hfst.ol',
            v3110 = '/homeappl/appl_taito/ling/hfst/3.11.0/share/hfst/fi/fi-analysis.hfst.ol',
            v3121 = '/homeappl/appl_taito/ling/hfst/3.12.1/share/hfst/fi/fi-analysis.hfst.ol')

import shutil
shutil.copy(them[Version], 'fi-analysis.hfst')
