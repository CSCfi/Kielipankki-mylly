# TOOL korp-info.py: "Get corpus info from Korp"
# (Queries korp.csc.fi for info on each corpus in a family)
# OUTPUT korp.info.json
# OUTPUT korp.info.tsv
# PARAMETER corpus TYPE [
#     COCA: "COCA",
#     COHA: "COHA",
#     EDUSKUNTA: "EDUSKUNTA",
#     S24: "S24",
#     S24samp: "S24samp",
#     YLILAUTA: "YLILAUTA"
# ] DEFAULT S24
# RUNTIME python3

# Turns out COCA and COHA require authentication so no go. Remove?

import json, os, sys
# os, sys are imported for testing - else chipster has them imported

# for testing! when outside chipster
# chipster_module_path = "home/jpiitula/proj/CSCfi/mylly/tools/kielipankki"
# corpus = "S24"

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_korp import request_info
import lib_names as names

# someone might want JSON, to use for something, or as a check
names.output('korp-info.json',
             'korp-{}.info.json'.format(corpus.lower()))

# but TSV is nicer to use in Mylly (for now anyway)
names.output('korp-info.tsv',
             'korp-{}.info.tsv'.format(corpus.lower()))

comma = ','

CORPORA = comma.join(dict(COCA = ("COCA_ACAD", "COCA_FIC", "COCA_MAG",
                                  "COCA_NEWS", "COCA_SPOK"),
                          
                          COHA =
                          ("COHA_1810S_FIC", "COHA_1810S_MAG",
                           "COHA_1810S_NF", "COHA_1820S_FIC",
                           "COHA_1820S_MAG", "COHA_1820S_NF",
                           "COHA_1830S_FIC", "COHA_1830S_MAG",
                           "COHA_1830S_NF", "COHA_1840S_FIC",
                           "COHA_1840S_MAG", "COHA_1840S_NF",
                           "COHA_1850S_FIC", "COHA_1850S_MAG",
                           "COHA_1850S_NF", "COHA_1860S_FIC",
                           "COHA_1860S_MAG", "COHA_1860S_NEWS",
                           "COHA_1860S_NF", "COHA_1870S_FIC",
                           "COHA_1870S_MAG", "COHA_1870S_NEWS",
                           "COHA_1870S_NF", "COHA_1880S_FIC",
                           "COHA_1880S_MAG", "COHA_1880S_NEWS",
                           "COHA_1880S_NF", "COHA_1890S_FIC",
                           "COHA_1890S_MAG", "COHA_1890S_NEWS",
                           "COHA_1890S_NF", "COHA_1900S_FIC",
                           "COHA_1900S_MAG", "COHA_1900S_NEWS",
                           "COHA_1900S_NF", "COHA_1910S_FIC",
                           "COHA_1910S_MAG", "COHA_1910S_NEWS",
                           "COHA_1910S_NF", "COHA_1920S_FIC",
                           "COHA_1920S_MAG", "COHA_1920S_NEWS",
                           "COHA_1920S_NF", "COHA_1930S_FIC",
                           "COHA_1930S_MAG", "COHA_1930S_NEWS",
                           "COHA_1930S_NF", "COHA_1940S_FIC",
                           "COHA_1940S_MAG", "COHA_1940S_NEWS",
                           "COHA_1940S_NF", "COHA_1950S_FIC",
                           "COHA_1950S_MAG", "COHA_1950S_NEWS",
                           "COHA_1950S_NF", "COHA_1960S_FIC",
                           "COHA_1960S_MAG", "COHA_1960S_NEWS",
                           "COHA_1960S_NF", "COHA_1970S_FIC",
                           "COHA_1970S_MAG", "COHA_1970S_NEWS",
                           "COHA_1970S_NF", "COHA_1980S_FIC",
                           "COHA_1980S_MAG", "COHA_1980S_NEWS",
                           "COHA_1980S_NF", "COHA_1990S_FIC",
                           "COHA_1990S_MAG", "COHA_1990S_NEWS",
                           "COHA_1990S_NF", "COHA_2000S_FIC",
                           "COHA_2000S_MAG", "COHA_2000S_NEWS",
                           "COHA_2000S_NF"),

                          EDUSKUNTA =
                          ("EDUSKUNTA",),

                          S24 =
                          ("S24_001",
                           "S24_002",
                           "S24_003",
                           "S24_004",
                           "S24_005",
                           "S24_006",
                           "S24_007",
                           "S24_008",
                           "S24_009",
                           "S24_010",
                           "S24_011"),

                          S24samp =
                          ("S24",), # right? näyte, eri kuin muut?

                          YLILAUTA =
                          ("YLILAUTA",))
                     
                     [corpus])

info = request_info(corpora = CORPORA)
               
with open('korp.info.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(info, result,
              ensure_ascii = False,
              check_circular = False)

# omitting attrs/a for now - need at least see an example first!
# (it has to do with alignment in parallel corpora, which learn)

with open('korp.info.tsv', mode = 'w', encoding = 'utf-8') as out:
    print('corpus', 'group', 'type', 'info', sep = '\t', file = out)
    for corpus, data in info['corpora'].items():
        for name in data['attrs']['p']:
            print(corpus, 'attrs', 'p', name, sep = '\t', file = out)
        for name in data['attrs']['s']:
            print(corpus, 'attrs', 's', name, sep = '\t', file = out)
        for key, value in data['info'].items():
            print(corpus, 'info', key, value, sep = '\t', file = out)
