# TOOL korp-kwic-vnsk.py: "VNSK concordance"
# (Search VNSK corpus in korp.csc.fi for a KWIC concordance. Query file contains CQP expressions that must match. The last expression defines Key Word. Concordance is saved in Korp JSON format.)
# INPUT query.cqp: "Query file" TYPE GENERIC
#     (One or more CQP expressions)
# OUTPUT result.json
# PARAMETER corpus: "Corpus" TYPE [
#   VNSK_AEJMELAEUS: "VNSK_AEJMELAEUS",
#   VNSK_AHLHOLM: "VNSK_AHLHOLM",
#   VNSK_AHLMAN_KIRJAT: "VNSK_AHLMAN_KIRJAT",
#   VNSK_AHLMAN_SANASTOT: "VNSK_AHLMAN_SANASTOT",
#   VNSK_AHLQVIST: "VNSK_AHLQVIST",
#   VNSK_AKIANDER: "VNSK_AKIANDER",
#   VNSK_ALMANAKKA: "VNSK_ALMANAKKA",
#   VNSK_AMINOFF: "VNSK_AMINOFF",
#   VNSK_ANONYYMI: "VNSK_ANONYYMI",
#   VNSK_ASETUS: "VNSK_ASETUS",
#   VNSK_AULEN: "VNSK_AULEN",
#   VNSK_BACKVALL: "VNSK_BACKVALL",
#   VNSK_BOCKER: "VNSK_BOCKER",
#   VNSK_BONSDORFF: "VNSK_BONSDORFF",
#   VNSK_BORENIUS: "VNSK_BORENIUS",
#   VNSK_BORG: "VNSK_BORG",
#   VNSK_CAJAN: "VNSK_CAJAN",
#   VNSK_CANNELIN: "VNSK_CANNELIN",
#   VNSK_CANTELL: "VNSK_CANTELL",
#   VNSK_CANTH: "VNSK_CANTH",
#   VNSK_CORANDER: "VNSK_CORANDER",
#   VNSK_COSTIANDER: "VNSK_COSTIANDER",
#   VNSK_DAHLBERG: "VNSK_DAHLBERG",
#   VNSK_EDLUND: "VNSK_EDLUND",
#   VNSK_EKLOF: "VNSK_EKLOF",
#   VNSK_EUREN: "VNSK_EUREN",
#   VNSK_EUROPAEUS: "VNSK_EUROPAEUS",
#   VNSK_EUROPAEUS_SANASTOT: "VNSK_EUROPAEUS_SANASTOT",
#   VNSK_FABRITIUS: "VNSK_FABRITIUS",
#   VNSK_FORSMAN: "VNSK_FORSMAN",
#   VNSK_FORSTROM: "VNSK_FORSTROM",
#   VNSK_FRIMAN: "VNSK_FRIMAN",
#   VNSK_FROSTERUS: "VNSK_FROSTERUS",
#   VNSK_GOTTLUND: "VNSK_GOTTLUND",
#   VNSK_GRANLUND: "VNSK_GRANLUND",
#   VNSK_HANNIKAINEN: "VNSK_HANNIKAINEN",
#   VNSK_HJELT: "VNSK_HJELT",
#   VNSK_HORDH: "VNSK_HORDH",
#   VNSK_HORNBORG: "VNSK_HORNBORG",
#   VNSK_IGNATIUS: "VNSK_IGNATIUS",
#   VNSK_INGMAN: "VNSK_INGMAN",
#   VNSK_INNAIN: "VNSK_INNAIN",
#   VNSK_JUTEINI: "VNSK_JUTEINI",
#   VNSK_KECKMAN: "VNSK_KECKMAN",
#   VNSK_KEMELL: "VNSK_KEMELL",
#   VNSK_KILPINEN: "VNSK_KILPINEN",
#   VNSK_KIVI: "VNSK_KIVI",
#   VNSK_KOSKINEN: "VNSK_KOSKINEN",
#   VNSK_KROHN: "VNSK_KROHN",
#   VNSK_LAGERVALL: "VNSK_LAGERVALL",
#   VNSK_LANKELA: "VNSK_LANKELA",
#   VNSK_LAVONIUS: "VNSK_LAVONIUS",
#   VNSK_LILIUS_ANTON: "VNSK_LILIUS_ANTON",
#   VNSK_LILIUS_AUKUSTI: "VNSK_LILIUS_AUKUSTI",
#   VNSK_LONNROT: "VNSK_LONNROT",
#   VNSK_MALMBERG: "VNSK_MALMBERG",
#   VNSK_MEHILAINEN: "VNSK_MEHILAINEN",
#   VNSK_MELA: "VNSK_MELA",
#   VNSK_MEURMAN: "VNSK_MEURMAN",
#   VNSK_MMY: "VNSK_MMY",
#   VNSK_MURMAN: "VNSK_MURMAN",
#   VNSK_MUUT: "VNSK_MUUT",
#   VNSK_NYMAN: "VNSK_NYMAN",
#   VNSK_OVS: "VNSK_OVS",
#   VNSK_POLEN: "VNSK_POLEN",
#   VNSK_POPPIUS: "VNSK_POPPIUS",
#   VNSK_PUHUTTELIJA: "VNSK_PUHUTTELIJA",
#   VNSK_REIN: "VNSK_REIN",
#   VNSK_ROOS: "VNSK_ROOS",
#   VNSK_SALMELAINEN: "VNSK_SALMELAINEN",
#   VNSK_SALONIUS: "VNSK_SALONIUS",
#   VNSK_SANALUETTELOT: "VNSK_SANALUETTELOT",
#   VNSK_SANDBERG: "VNSK_SANDBERG",
#   VNSK_SCHROTER: "VNSK_SCHROTER",
#   VNSK_SIRELIUS: "VNSK_SIRELIUS",
#   VNSK_SKOGMAN: "VNSK_SKOGMAN",
#   VNSK_SMTR: "VNSK_SMTR",
#   VNSK_SOHLBERG: "VNSK_SOHLBERG",
#   VNSK_SOLDAN: "VNSK_SOLDAN",
#   VNSK_SSV: "VNSK_SSV",
#   VNSK_STAHLBERG: "VNSK_STAHLBERG",
#   VNSK_TARVANEN: "VNSK_TARVANEN",
#   VNSK_TICKLEN: "VNSK_TICKLEN",
#   VNSK_TIKKANEN: "VNSK_TIKKANEN",
#   VNSK_TOPELIUS: "VNSK_TOPELIUS",
#   VNSK_TOPPELIUS: "VNSK_TOPPELIUS",
#   VNSK_TVS: "VNSK_TVS",
#   VNSK_VARELIUS: "VNSK_VARELIUS",
#   VNSK_VIRSIKIRJA: "VNSK_VIRSIKIRJA",
#   VNSK_WALLIN: "VNSK_WALLIN",
#   VNSK_WIKMAN: "VNSK_WIKMAN",
#   VNSK_WIWOLIN: "VNSK_WIWOLIN",
#   VNSK_YKSITT: "VNSK_YKSITT"
# ] DEFAULT VNSK_ANONYYMI
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999
#     (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0
#     (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)

# This tool specifies attributes for a particular corpus.

import json, math, random

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_korp import parse_queries, request_kwic
from lib_names2 import base, name

seed = random.randrange(1000, 10000) if math.isnan(seed) else seed

name('result.json', base('query.cqp', '*.cqp.txt'),
     ins = 'kwic-{}-s{}-p{}'.format(corpus, seed, page),
     ext = 'korp.json')

comma = ','

CORPUS = corpus

ANNO = comma.join('''

    word

'''.split())

META = comma.join('''

    paragraph paragraph_id sentence sentence_id text text_datefrom
    text_dateto text_distributor text_source text_title

    '''.split())

QUERIES = parse_queries('query.cqp')

kwic = request_kwic(corpus = CORPUS,
                    seed = seed,
                    size = 1000,
                    page = page,
                    anno = ANNO,
                    meta = META,
                    queries = QUERIES)

# note: it *adds* dict(M = dict(origin = size * page)) to the kwic

with open('result.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(kwic, result,
              ensure_ascii = False,
              check_circular = False)
