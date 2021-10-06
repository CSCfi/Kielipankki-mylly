# TOOL korp-info.py: "Corpus info"
# (Get info about a selected corpus family from korp.csc.fi)
# OUTPUT info.json
# OUTPUT info.tsv
# PARAMETER corpus: "Corpus" TYPE [
#     COCA: "COCA",
#     COHA: "COHA",
#     EDUSKUNTA: "EDUSKUNTA",
#     KLK_FI: "KLK_FI",
#     KLK_SV: "KLK_SV",
#     S24: "S24",
#     S24samp: "S24samp",
#     VKS: "VKS",
#     VNS: "VNS",
#     VNSK: "VNSK",
#     YLILAUTA: "YLILAUTA"
# ]
# IMAGE comp-16.04-mylly
# RUNTIME python3

# Turns out COCA and COHA require authentication so no go. Remove?

import json, os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_korp import request_info
from lib_names2 import name

# someone might want JSON, to use for something, or as a check
names.output('info.json',
             'info-{}.json'.format(corpus.lower()))

# but TSV is nicer to use in Mylly (for now anyway)
names.output('info.tsv',
             'info-{}.tsv'.format(corpus.lower()))

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
                          
	                  KLK_FI =
	                  ("KLK_FI_1820", "KLK_FI_1821", "KLK_FI_1822", "KLK_FI_1823",
	                   "KLK_FI_1824", "KLK_FI_1825", "KLK_FI_1826", "KLK_FI_1827",
	                   "KLK_FI_1829", "KLK_FI_1830", "KLK_FI_1831", "KLK_FI_1832",
	                   "KLK_FI_1833", "KLK_FI_1834", "KLK_FI_1835", "KLK_FI_1836",
	                   "KLK_FI_1837", "KLK_FI_1838", "KLK_FI_1839", "KLK_FI_1840",
	                   "KLK_FI_1841", "KLK_FI_1842", "KLK_FI_1844", "KLK_FI_1845",
	                   "KLK_FI_1846", "KLK_FI_1847", "KLK_FI_1848", "KLK_FI_1849",
	                   "KLK_FI_1850", "KLK_FI_1851", "KLK_FI_1852", "KLK_FI_1853",
	                   "KLK_FI_1854", "KLK_FI_1855", "KLK_FI_1856", "KLK_FI_1857",
	                   "KLK_FI_1858", "KLK_FI_1859", "KLK_FI_1860", "KLK_FI_1861",
	                   "KLK_FI_1862", "KLK_FI_1863", "KLK_FI_1864", "KLK_FI_1865",
	                   "KLK_FI_1866", "KLK_FI_1867", "KLK_FI_1868", "KLK_FI_1869",
	                   "KLK_FI_1870", "KLK_FI_1871", "KLK_FI_1872", "KLK_FI_1873",
	                   "KLK_FI_1874", "KLK_FI_1875", "KLK_FI_1876", "KLK_FI_1877",
	                   "KLK_FI_1878", "KLK_FI_1879", "KLK_FI_1880", "KLK_FI_1881",
	                   "KLK_FI_1882", "KLK_FI_1883", "KLK_FI_1884", "KLK_FI_1885",
	                   "KLK_FI_1886", "KLK_FI_1887", "KLK_FI_1888", "KLK_FI_1889",
	                   "KLK_FI_1890", "KLK_FI_1891", "KLK_FI_1892", "KLK_FI_1893",
	                   "KLK_FI_1894", "KLK_FI_1895", "KLK_FI_1896", "KLK_FI_1897",
	                   "KLK_FI_1898", "KLK_FI_1899", "KLK_FI_1900", "KLK_FI_1901",
	                   "KLK_FI_1902", "KLK_FI_1903", "KLK_FI_1904", "KLK_FI_1905",
	                   "KLK_FI_1906", "KLK_FI_1907", "KLK_FI_1908", "KLK_FI_1909",
	                   "KLK_FI_1910", "KLK_FI_1911", "KLK_FI_1912", "KLK_FI_1913",
	                   "KLK_FI_1914", "KLK_FI_1915", "KLK_FI_1916", "KLK_FI_1917",
	                   "KLK_FI_1918", "KLK_FI_1919", "KLK_FI_1920", "KLK_FI_1921",
	                   "KLK_FI_1922", "KLK_FI_1923", "KLK_FI_1924", "KLK_FI_1925",
	                   "KLK_FI_1926", "KLK_FI_1927", "KLK_FI_1928", "KLK_FI_1929",
	                   "KLK_FI_1930", "KLK_FI_1931", "KLK_FI_1932", "KLK_FI_1933",
	                   "KLK_FI_1934", "KLK_FI_1935", "KLK_FI_1936", "KLK_FI_1937",
	                   "KLK_FI_1938", "KLK_FI_1939", "KLK_FI_1940", "KLK_FI_1941",
	                   "KLK_FI_1942", "KLK_FI_1943", "KLK_FI_1944", "KLK_FI_1945",
	                   "KLK_FI_1946", "KLK_FI_1947", "KLK_FI_1948", "KLK_FI_1949",
	                   "KLK_FI_1950", "KLK_FI_1951", "KLK_FI_1952", "KLK_FI_1953",
	                   "KLK_FI_1954", "KLK_FI_1955", "KLK_FI_1956", "KLK_FI_1957",
	                   "KLK_FI_1958", "KLK_FI_1959", "KLK_FI_1960", "KLK_FI_1961",
	                   "KLK_FI_1962", "KLK_FI_1963", "KLK_FI_1964", "KLK_FI_1965",
	                   "KLK_FI_1966", "KLK_FI_1967", "KLK_FI_1968", "KLK_FI_1969",
	                   "KLK_FI_1970", "KLK_FI_1971", "KLK_FI_1972", "KLK_FI_1973",
	                   "KLK_FI_1974", "KLK_FI_1975", "KLK_FI_1976", "KLK_FI_1977",
	                   "KLK_FI_1978", "KLK_FI_1979", "KLK_FI_1980", "KLK_FI_1981",
	                   "KLK_FI_1982", "KLK_FI_1983", "KLK_FI_1984", "KLK_FI_1985",
	                   "KLK_FI_1986", "KLK_FI_1987", "KLK_FI_1988", "KLK_FI_1989",
	                   "KLK_FI_1990", "KLK_FI_1991", "KLK_FI_1992", "KLK_FI_1993",
	                   "KLK_FI_1994", "KLK_FI_1995", "KLK_FI_1996", "KLK_FI_1997",
	                   "KLK_FI_1998", "KLK_FI_1999", "KLK_FI_2000", "KLK_FI_2011"),
                          # "KLK_FI_2011" has different attributes 2017-09-25
                          
	                  KLK_SV =
                          
	                  ("KLK_SV_1771", "KLK_SV_1772", "KLK_SV_1773", "KLK_SV_1774",
	                   "KLK_SV_1775", "KLK_SV_1776", "KLK_SV_1777", "KLK_SV_1778",
	                   "KLK_SV_1782", "KLK_SV_1783", "KLK_SV_1784", "KLK_SV_1785",
	                   "KLK_SV_1789", "KLK_SV_1791", "KLK_SV_1792", "KLK_SV_1793",
	                   "KLK_SV_1794", "KLK_SV_1795", "KLK_SV_1796", "KLK_SV_1797",
	                   "KLK_SV_1798", "KLK_SV_1799", "KLK_SV_1800", "KLK_SV_1801",
	                   "KLK_SV_1802", "KLK_SV_1803", "KLK_SV_1804", "KLK_SV_1805",
	                   "KLK_SV_1806", "KLK_SV_1807", "KLK_SV_1808", "KLK_SV_1809",
	                   "KLK_SV_1810", "KLK_SV_1811", "KLK_SV_1812", "KLK_SV_1813",
	                   "KLK_SV_1814", "KLK_SV_1815", "KLK_SV_1816", "KLK_SV_1817",
	                   "KLK_SV_1818", "KLK_SV_1819", "KLK_SV_1820", "KLK_SV_1821",
	                   "KLK_SV_1822", "KLK_SV_1823", "KLK_SV_1824", "KLK_SV_1825",
	                   "KLK_SV_1826", "KLK_SV_1827", "KLK_SV_1828", "KLK_SV_1829",
	                   "KLK_SV_1830", "KLK_SV_1831", "KLK_SV_1832", "KLK_SV_1833",
	                   "KLK_SV_1834", "KLK_SV_1835", "KLK_SV_1836", "KLK_SV_1837",
	                   "KLK_SV_1838", "KLK_SV_1839", "KLK_SV_1840", "KLK_SV_1841",
	                   "KLK_SV_1842", "KLK_SV_1843", "KLK_SV_1844", "KLK_SV_1845",
	                   "KLK_SV_1846", "KLK_SV_1847", "KLK_SV_1848", "KLK_SV_1849",
	                   "KLK_SV_1850", "KLK_SV_1851", "KLK_SV_1852", "KLK_SV_1853",
	                   "KLK_SV_1854", "KLK_SV_1855", "KLK_SV_1856", "KLK_SV_1857",
	                   "KLK_SV_1858", "KLK_SV_1859", "KLK_SV_1860", "KLK_SV_1861",
	                   "KLK_SV_1862", "KLK_SV_1863", "KLK_SV_1864", "KLK_SV_1865",
	                   "KLK_SV_1866", "KLK_SV_1867", "KLK_SV_1868", "KLK_SV_1869",
	                   "KLK_SV_1870", "KLK_SV_1871", "KLK_SV_1872", "KLK_SV_1873",
	                   "KLK_SV_1874", "KLK_SV_1875", "KLK_SV_1876", "KLK_SV_1877",
	                   "KLK_SV_1878", "KLK_SV_1879", "KLK_SV_1880", "KLK_SV_1881",
	                   "KLK_SV_1882", "KLK_SV_1883", "KLK_SV_1884", "KLK_SV_1885",
	                   "KLK_SV_1886", "KLK_SV_1887", "KLK_SV_1888", "KLK_SV_1889",
	                   "KLK_SV_1890", "KLK_SV_1891", "KLK_SV_1892", "KLK_SV_1893",
	                   "KLK_SV_1894", "KLK_SV_1895", "KLK_SV_1896", "KLK_SV_1897",
	                   "KLK_SV_1898", "KLK_SV_1899", "KLK_SV_1900", "KLK_SV_1901",
	                   "KLK_SV_1902", "KLK_SV_1903", "KLK_SV_1904", "KLK_SV_1905",
	                   "KLK_SV_1906", "KLK_SV_1907", "KLK_SV_1908", "KLK_SV_1909",
	                   "KLK_SV_1910", "KLK_SV_1911", "KLK_SV_1912", "KLK_SV_1913",
	                   "KLK_SV_1914", "KLK_SV_1915", "KLK_SV_1916", "KLK_SV_1917",
	                   "KLK_SV_1918", "KLK_SV_1919", "KLK_SV_1920", "KLK_SV_1921",
	                   "KLK_SV_1922", "KLK_SV_1923", "KLK_SV_1924", "KLK_SV_1925",
	                   "KLK_SV_1926", "KLK_SV_1927", "KLK_SV_1928", "KLK_SV_1929",
	                   "KLK_SV_1930", "KLK_SV_1931", "KLK_SV_1932", "KLK_SV_1933",
	                   "KLK_SV_1934", "KLK_SV_1935", "KLK_SV_1936", "KLK_SV_1937",
	                   "KLK_SV_1938", "KLK_SV_1939", "KLK_SV_1940", "KLK_SV_1941",
	                   "KLK_SV_1942", "KLK_SV_1943", "KLK_SV_1944", "KLK_SV_1945",
	                   "KLK_SV_1946", "KLK_SV_1947", "KLK_SV_1948", "KLK_SV_1982",
	                   "KLK_SV_1983", "KLK_SV_1986"),
                          
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
                          
                          VKS =
                          ("VKS_AGRICOLA",
                           "VKS_ALMANAKAT",
                           "VKS_BIBLIA",
                           "VKS_BJORKQVIST",
                           "VKS_FROSTERUS",
                           "VKS_GANANDER",
                           "VKS_LAIT",
                           "VKS_LIZELIUS",
                           "VKS_LPETRI",
                           "VKS_SAARNAT",
                           "VKS_VARIA",
                           "VKS_VIRRET"),
                          
                          VNSK =
                          ("VNSK_AEJMELAEUS",
                           "VNSK_AHLHOLM",
                           "VNSK_AHLMAN_KIRJAT",
                           "VNSK_AHLMAN_SANASTOT",
                           "VNSK_AHLQVIST",
                           "VNSK_AKIANDER",
                           "VNSK_ALMANAKKA",
                           "VNSK_AMINOFF",
                           "VNSK_ANONYYMI",
                           "VNSK_ASETUS",
                           "VNSK_AULEN",
                           "VNSK_BACKVALL",
                           "VNSK_BOCKER",
                           "VNSK_BONSDORFF",
                           "VNSK_BORENIUS",
                           "VNSK_BORG",
                           "VNSK_CAJAN",
                           "VNSK_CANNELIN",
                           "VNSK_CANTELL",
                           "VNSK_CANTH",
                           "VNSK_CORANDER",
                           "VNSK_COSTIANDER",
                           "VNSK_DAHLBERG",
                           "VNSK_EDLUND",
                           "VNSK_EKLOF",
                           "VNSK_EUREN",
                           "VNSK_EUROPAEUS",
                           "VNSK_EUROPAEUS_SANASTOT",
                           "VNSK_FABRITIUS",
                           "VNSK_FORSMAN",
                           "VNSK_FORSTROM",
                           "VNSK_FRIMAN",
                           "VNSK_FROSTERUS",
                           "VNSK_GOTTLUND",
                           "VNSK_GRANLUND",
                           "VNSK_HANNIKAINEN",
                           "VNSK_HJELT",
                           "VNSK_HORDH",
                           "VNSK_HORNBORG",
                           "VNSK_IGNATIUS",
                           "VNSK_INGMAN",
                           "VNSK_INNAIN",
                           "VNSK_JUTEINI",
                           "VNSK_KECKMAN",
                           "VNSK_KEMELL",
                           "VNSK_KILPINEN",
                           "VNSK_KIVI",
                           "VNSK_KOSKINEN",
                           "VNSK_KROHN",
                           "VNSK_LAGERVALL",
                           "VNSK_LANKELA",
                           "VNSK_LAVONIUS",
                           "VNSK_LILIUS_ANTON",
                           "VNSK_LILIUS_AUKUSTI",
                           "VNSK_LONNROT",
                           "VNSK_MALMBERG",
                           "VNSK_MEHILAINEN",
                           "VNSK_MELA",
                           "VNSK_MEURMAN",
                           "VNSK_MMY",
                           "VNSK_MURMAN",
                           "VNSK_MUUT",
                           "VNSK_NYMAN",
                           "VNSK_OVS",
                           "VNSK_POLEN",
                           "VNSK_POPPIUS",
                           "VNSK_PUHUTTELIJA",
                           "VNSK_REIN",
                           "VNSK_ROOS",
                           "VNSK_SALMELAINEN",
                           "VNSK_SALONIUS",
                           "VNSK_SANALUETTELOT",
                           "VNSK_SANDBERG",
                           "VNSK_SCHROTER",
                           "VNSK_SIRELIUS",
                           "VNSK_SKOGMAN",
                           "VNSK_SMTR",
                           "VNSK_SOHLBERG",
                           "VNSK_SOLDAN",
                           "VNSK_SSV",
                           "VNSK_STAHLBERG",
                           "VNSK_TARVANEN",
                           "VNSK_TICKLEN",
                           "VNSK_TIKKANEN",
                           "VNSK_TOPELIUS",
                           "VNSK_TOPPELIUS",
                           "VNSK_TVS",
                           "VNSK_VARELIUS",
                           "VNSK_VIRSIKIRJA",
                           "VNSK_WALLIN",
                           "VNSK_WIKMAN",
                           "VNSK_WIWOLIN",
                           "VNSK_YKSITT"),
                          
                          VNS = 
                          ("VNS_ASETUS",
                           "VNS_RENQVIST",
                           "VNS_RENVALL"),
                          
                          YLILAUTA =
                          ("YLILAUTA",))
                     
                     [corpus])

info = request_info(corpora = CORPORA)
               
with open('info.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(info, result,
              ensure_ascii = False,
              check_circular = False)

# omitting attrs/a for now - need at least see an example first!
# (it has to do with alignment in parallel corpora, which learn)

with open('info.tsv', mode = 'w', encoding = 'utf-8') as out:
    print('corpus', 'group', 'type', 'info', sep = '\t', file = out)
    for corpus, data in info['corpora'].items():
        for name in data['attrs']['p']:
            print(corpus, 'attrs', 'p', name, sep = '\t', file = out)
        for name in data['attrs']['s']:
            print(corpus, 'attrs', 's', name, sep = '\t', file = out)
        for key, value in data['info'].items():
            print(corpus, 'info', key, value, sep = '\t', file = out)
