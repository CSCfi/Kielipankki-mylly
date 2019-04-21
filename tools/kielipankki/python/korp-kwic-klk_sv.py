# TOOL korp-kwic-klk_sv.py: " KLK_SV KWIC"
# (Search KLK_SV corpus in korp.csc.fi for a KWIC concordance. Query file contains CQP expressions that must match. The last expression defines Key Word. Concordance is saved in Korp JSON format.)
# INPUT query.cqp: "Query file" TYPE GENERIC
#     (One or more CQP expressions)
# OUTPUT result.json
# PARAMETER corpus: "Corpus" TYPE [
#   KLK_SV_1771: "KLK_SV_1771",
#   KLK_SV_1772: "KLK_SV_1772",
#   KLK_SV_1773: "KLK_SV_1773",
#   KLK_SV_1774: "KLK_SV_1774",
#   KLK_SV_1775: "KLK_SV_1775",
#   KLK_SV_1776: "KLK_SV_1776",
#   KLK_SV_1777: "KLK_SV_1777",
#   KLK_SV_1778: "KLK_SV_1778",
#   KLK_SV_1782: "KLK_SV_1782",
#   KLK_SV_1783: "KLK_SV_1783",
#   KLK_SV_1784: "KLK_SV_1784",
#   KLK_SV_1785: "KLK_SV_1785",
#   KLK_SV_1789: "KLK_SV_1789",
#   KLK_SV_1791: "KLK_SV_1791",
#   KLK_SV_1792: "KLK_SV_1792",
#   KLK_SV_1793: "KLK_SV_1793",
#   KLK_SV_1794: "KLK_SV_1794",
#   KLK_SV_1795: "KLK_SV_1795",
#   KLK_SV_1796: "KLK_SV_1796",
#   KLK_SV_1797: "KLK_SV_1797",
#   KLK_SV_1798: "KLK_SV_1798",
#   KLK_SV_1799: "KLK_SV_1799",
#   KLK_SV_1800: "KLK_SV_1800",
#   KLK_SV_1801: "KLK_SV_1801",
#   KLK_SV_1802: "KLK_SV_1802",
#   KLK_SV_1803: "KLK_SV_1803",
#   KLK_SV_1804: "KLK_SV_1804",
#   KLK_SV_1805: "KLK_SV_1805",
#   KLK_SV_1806: "KLK_SV_1806",
#   KLK_SV_1807: "KLK_SV_1807",
#   KLK_SV_1808: "KLK_SV_1808",
#   KLK_SV_1809: "KLK_SV_1809",
#   KLK_SV_1810: "KLK_SV_1810",
#   KLK_SV_1811: "KLK_SV_1811",
#   KLK_SV_1812: "KLK_SV_1812",
#   KLK_SV_1813: "KLK_SV_1813",
#   KLK_SV_1814: "KLK_SV_1814",
#   KLK_SV_1815: "KLK_SV_1815",
#   KLK_SV_1816: "KLK_SV_1816",
#   KLK_SV_1817: "KLK_SV_1817",
#   KLK_SV_1818: "KLK_SV_1818",
#   KLK_SV_1819: "KLK_SV_1819",
#   KLK_SV_1820: "KLK_SV_1820",
#   KLK_SV_1821: "KLK_SV_1821",
#   KLK_SV_1822: "KLK_SV_1822",
#   KLK_SV_1823: "KLK_SV_1823",
#   KLK_SV_1824: "KLK_SV_1824",
#   KLK_SV_1825: "KLK_SV_1825",
#   KLK_SV_1826: "KLK_SV_1826",
#   KLK_SV_1827: "KLK_SV_1827",
#   KLK_SV_1828: "KLK_SV_1828",
#   KLK_SV_1829: "KLK_SV_1829",
#   KLK_SV_1830: "KLK_SV_1830",
#   KLK_SV_1831: "KLK_SV_1831",
#   KLK_SV_1832: "KLK_SV_1832",
#   KLK_SV_1833: "KLK_SV_1833",
#   KLK_SV_1834: "KLK_SV_1834",
#   KLK_SV_1835: "KLK_SV_1835",
#   KLK_SV_1836: "KLK_SV_1836",
#   KLK_SV_1837: "KLK_SV_1837",
#   KLK_SV_1838: "KLK_SV_1838",
#   KLK_SV_1839: "KLK_SV_1839",
#   KLK_SV_1840: "KLK_SV_1840",
#   KLK_SV_1841: "KLK_SV_1841",
#   KLK_SV_1842: "KLK_SV_1842",
#   KLK_SV_1843: "KLK_SV_1843",
#   KLK_SV_1844: "KLK_SV_1844",
#   KLK_SV_1845: "KLK_SV_1845",
#   KLK_SV_1846: "KLK_SV_1846",
#   KLK_SV_1847: "KLK_SV_1847",
#   KLK_SV_1848: "KLK_SV_1848",
#   KLK_SV_1849: "KLK_SV_1849",
#   KLK_SV_1850: "KLK_SV_1850",
#   KLK_SV_1851: "KLK_SV_1851",
#   KLK_SV_1852: "KLK_SV_1852",
#   KLK_SV_1853: "KLK_SV_1853",
#   KLK_SV_1854: "KLK_SV_1854",
#   KLK_SV_1855: "KLK_SV_1855",
#   KLK_SV_1856: "KLK_SV_1856",
#   KLK_SV_1857: "KLK_SV_1857",
#   KLK_SV_1858: "KLK_SV_1858",
#   KLK_SV_1859: "KLK_SV_1859",
#   KLK_SV_1860: "KLK_SV_1860",
#   KLK_SV_1861: "KLK_SV_1861",
#   KLK_SV_1862: "KLK_SV_1862",
#   KLK_SV_1863: "KLK_SV_1863",
#   KLK_SV_1864: "KLK_SV_1864",
#   KLK_SV_1865: "KLK_SV_1865",
#   KLK_SV_1866: "KLK_SV_1866",
#   KLK_SV_1867: "KLK_SV_1867",
#   KLK_SV_1868: "KLK_SV_1868",
#   KLK_SV_1869: "KLK_SV_1869",
#   KLK_SV_1870: "KLK_SV_1870",
#   KLK_SV_1871: "KLK_SV_1871",
#   KLK_SV_1872: "KLK_SV_1872",
#   KLK_SV_1873: "KLK_SV_1873",
#   KLK_SV_1874: "KLK_SV_1874",
#   KLK_SV_1875: "KLK_SV_1875",
#   KLK_SV_1876: "KLK_SV_1876",
#   KLK_SV_1877: "KLK_SV_1877",
#   KLK_SV_1878: "KLK_SV_1878",
#   KLK_SV_1879: "KLK_SV_1879",
#   KLK_SV_1880: "KLK_SV_1880",
#   KLK_SV_1881: "KLK_SV_1881",
#   KLK_SV_1882: "KLK_SV_1882",
#   KLK_SV_1883: "KLK_SV_1883",
#   KLK_SV_1884: "KLK_SV_1884",
#   KLK_SV_1885: "KLK_SV_1885",
#   KLK_SV_1886: "KLK_SV_1886",
#   KLK_SV_1887: "KLK_SV_1887",
#   KLK_SV_1888: "KLK_SV_1888",
#   KLK_SV_1889: "KLK_SV_1889",
#   KLK_SV_1890: "KLK_SV_1890",
#   KLK_SV_1891: "KLK_SV_1891",
#   KLK_SV_1892: "KLK_SV_1892",
#   KLK_SV_1893: "KLK_SV_1893",
#   KLK_SV_1894: "KLK_SV_1894",
#   KLK_SV_1895: "KLK_SV_1895",
#   KLK_SV_1896: "KLK_SV_1896",
#   KLK_SV_1897: "KLK_SV_1897",
#   KLK_SV_1898: "KLK_SV_1898",
#   KLK_SV_1899: "KLK_SV_1899",
#   KLK_SV_1900: "KLK_SV_1900",
#   KLK_SV_1901: "KLK_SV_1901",
#   KLK_SV_1902: "KLK_SV_1902",
#   KLK_SV_1903: "KLK_SV_1903",
#   KLK_SV_1904: "KLK_SV_1904",
#   KLK_SV_1905: "KLK_SV_1905",
#   KLK_SV_1906: "KLK_SV_1906",
#   KLK_SV_1907: "KLK_SV_1907",
#   KLK_SV_1908: "KLK_SV_1908",
#   KLK_SV_1909: "KLK_SV_1909",
#   KLK_SV_1910: "KLK_SV_1910",
#   KLK_SV_1911: "KLK_SV_1911",
#   KLK_SV_1912: "KLK_SV_1912",
#   KLK_SV_1913: "KLK_SV_1913",
#   KLK_SV_1914: "KLK_SV_1914",
#   KLK_SV_1915: "KLK_SV_1915",
#   KLK_SV_1916: "KLK_SV_1916",
#   KLK_SV_1917: "KLK_SV_1917",
#   KLK_SV_1918: "KLK_SV_1918",
#   KLK_SV_1919: "KLK_SV_1919",
#   KLK_SV_1920: "KLK_SV_1920",
#   KLK_SV_1921: "KLK_SV_1921",
#   KLK_SV_1922: "KLK_SV_1922",
#   KLK_SV_1923: "KLK_SV_1923",
#   KLK_SV_1924: "KLK_SV_1924",
#   KLK_SV_1925: "KLK_SV_1925",
#   KLK_SV_1926: "KLK_SV_1926",
#   KLK_SV_1927: "KLK_SV_1927",
#   KLK_SV_1928: "KLK_SV_1928",
#   KLK_SV_1929: "KLK_SV_1929",
#   KLK_SV_1930: "KLK_SV_1930",
#   KLK_SV_1931: "KLK_SV_1931",
#   KLK_SV_1932: "KLK_SV_1932",
#   KLK_SV_1933: "KLK_SV_1933",
#   KLK_SV_1934: "KLK_SV_1934",
#   KLK_SV_1935: "KLK_SV_1935",
#   KLK_SV_1936: "KLK_SV_1936",
#   KLK_SV_1937: "KLK_SV_1937",
#   KLK_SV_1938: "KLK_SV_1938",
#   KLK_SV_1939: "KLK_SV_1939",
#   KLK_SV_1940: "KLK_SV_1940",
#   KLK_SV_1941: "KLK_SV_1941",
#   KLK_SV_1942: "KLK_SV_1942",
#   KLK_SV_1943: "KLK_SV_1943",
#   KLK_SV_1944: "KLK_SV_1944",
#   KLK_SV_1945: "KLK_SV_1945",
#   KLK_SV_1946: "KLK_SV_1946",
#   KLK_SV_1947: "KLK_SV_1947",
#   KLK_SV_1948: "KLK_SV_1948",
#   KLK_SV_1982: "KLK_SV_1982",
#   KLK_SV_1983: "KLK_SV_1983",
#   KLK_SV_1986: "KLK_SV_1986"
# ] DEFAULT KLK_SV_1917
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999
#     (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0
#     (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)
# RUNTIME python3

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

        dephead deprel lemma lex msd ocr pos prefix ref saldo style
        suffix word

'''.split())

META = comma.join('''

        paragraph_n sentence_id sentence_n text_binding_id
        text_datefrom text_dateto text_elec_date text_file
        text_img_url text_issue_date text_issue_no text_issue_title
        text_label text_language text_page_id text_page_no
        text_part_name text_publ_id text_publ_part text_publ_title
        text_publ_type text_sentcount text_timefrom text_timeto
        text_tokencount

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
