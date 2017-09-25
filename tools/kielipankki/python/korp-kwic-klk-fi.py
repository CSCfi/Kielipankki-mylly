# TOOL korp-kwic-klk_fi.py: "Get Korp KWIC concordance from KLK_FI corpus"
# (Queries korp.csc.fi for a KWIC concordance from KLK_FI corpus. Input file contains CQP expressions separated by empty lines. They must all match. The last of them defines the final match. Output file is the concordance in the Korp JSON form.)
# INPUT query.cqp.txt TYPE GENERIC
# OUTPUT result.korp.json
# PARAMETER corpus TYPE [
#   KLK_FI_1820: "KLK_FI_1820",
#   KLK_FI_1821: "KLK_FI_1821",
#   KLK_FI_1822: "KLK_FI_1822",
#   KLK_FI_1823: "KLK_FI_1823",
#   KLK_FI_1824: "KLK_FI_1824",
#   KLK_FI_1825: "KLK_FI_1825",
#   KLK_FI_1826: "KLK_FI_1826",
#   KLK_FI_1827: "KLK_FI_1827",
#   KLK_FI_1829: "KLK_FI_1829",
#   KLK_FI_1830: "KLK_FI_1830",
#   KLK_FI_1831: "KLK_FI_1831",
#   KLK_FI_1832: "KLK_FI_1832",
#   KLK_FI_1833: "KLK_FI_1833",
#   KLK_FI_1834: "KLK_FI_1834",
#   KLK_FI_1835: "KLK_FI_1835",
#   KLK_FI_1836: "KLK_FI_1836",
#   KLK_FI_1837: "KLK_FI_1837",
#   KLK_FI_1838: "KLK_FI_1838",
#   KLK_FI_1839: "KLK_FI_1839",
#   KLK_FI_1840: "KLK_FI_1840",
#   KLK_FI_1841: "KLK_FI_1841",
#   KLK_FI_1842: "KLK_FI_1842",
#   KLK_FI_1844: "KLK_FI_1844",
#   KLK_FI_1845: "KLK_FI_1845",
#   KLK_FI_1846: "KLK_FI_1846",
#   KLK_FI_1847: "KLK_FI_1847",
#   KLK_FI_1848: "KLK_FI_1848",
#   KLK_FI_1849: "KLK_FI_1849",
#   KLK_FI_1850: "KLK_FI_1850",
#   KLK_FI_1851: "KLK_FI_1851",
#   KLK_FI_1852: "KLK_FI_1852",
#   KLK_FI_1853: "KLK_FI_1853",
#   KLK_FI_1854: "KLK_FI_1854",
#   KLK_FI_1855: "KLK_FI_1855",
#   KLK_FI_1856: "KLK_FI_1856",
#   KLK_FI_1857: "KLK_FI_1857",
#   KLK_FI_1858: "KLK_FI_1858",
#   KLK_FI_1859: "KLK_FI_1859",
#   KLK_FI_1860: "KLK_FI_1860",
#   KLK_FI_1861: "KLK_FI_1861",
#   KLK_FI_1862: "KLK_FI_1862",
#   KLK_FI_1863: "KLK_FI_1863",
#   KLK_FI_1864: "KLK_FI_1864",
#   KLK_FI_1865: "KLK_FI_1865",
#   KLK_FI_1866: "KLK_FI_1866",
#   KLK_FI_1867: "KLK_FI_1867",
#   KLK_FI_1868: "KLK_FI_1868",
#   KLK_FI_1869: "KLK_FI_1869",
#   KLK_FI_1870: "KLK_FI_1870",
#   KLK_FI_1871: "KLK_FI_1871",
#   KLK_FI_1872: "KLK_FI_1872",
#   KLK_FI_1873: "KLK_FI_1873",
#   KLK_FI_1874: "KLK_FI_1874",
#   KLK_FI_1875: "KLK_FI_1875",
#   KLK_FI_1876: "KLK_FI_1876",
#   KLK_FI_1877: "KLK_FI_1877",
#   KLK_FI_1878: "KLK_FI_1878",
#   KLK_FI_1879: "KLK_FI_1879",
#   KLK_FI_1880: "KLK_FI_1880",
#   KLK_FI_1881: "KLK_FI_1881",
#   KLK_FI_1882: "KLK_FI_1882",
#   KLK_FI_1883: "KLK_FI_1883",
#   KLK_FI_1884: "KLK_FI_1884",
#   KLK_FI_1885: "KLK_FI_1885",
#   KLK_FI_1886: "KLK_FI_1886",
#   KLK_FI_1887: "KLK_FI_1887",
#   KLK_FI_1888: "KLK_FI_1888",
#   KLK_FI_1889: "KLK_FI_1889",
#   KLK_FI_1890: "KLK_FI_1890",
#   KLK_FI_1891: "KLK_FI_1891",
#   KLK_FI_1892: "KLK_FI_1892",
#   KLK_FI_1893: "KLK_FI_1893",
#   KLK_FI_1894: "KLK_FI_1894",
#   KLK_FI_1895: "KLK_FI_1895",
#   KLK_FI_1896: "KLK_FI_1896",
#   KLK_FI_1897: "KLK_FI_1897",
#   KLK_FI_1898: "KLK_FI_1898",
#   KLK_FI_1899: "KLK_FI_1899",
#   KLK_FI_1900: "KLK_FI_1900",
#   KLK_FI_1901: "KLK_FI_1901",
#   KLK_FI_1902: "KLK_FI_1902",
#   KLK_FI_1903: "KLK_FI_1903",
#   KLK_FI_1904: "KLK_FI_1904",
#   KLK_FI_1905: "KLK_FI_1905",
#   KLK_FI_1906: "KLK_FI_1906",
#   KLK_FI_1907: "KLK_FI_1907",
#   KLK_FI_1908: "KLK_FI_1908",
#   KLK_FI_1909: "KLK_FI_1909",
#   KLK_FI_1910: "KLK_FI_1910",
#   KLK_FI_1911: "KLK_FI_1911",
#   KLK_FI_1912: "KLK_FI_1912",
#   KLK_FI_1913: "KLK_FI_1913",
#   KLK_FI_1914: "KLK_FI_1914",
#   KLK_FI_1915: "KLK_FI_1915",
#   KLK_FI_1916: "KLK_FI_1916",
#   KLK_FI_1917: "KLK_FI_1917",
#   KLK_FI_1918: "KLK_FI_1918",
#   KLK_FI_1919: "KLK_FI_1919",
#   KLK_FI_1920: "KLK_FI_1920",
#   KLK_FI_1921: "KLK_FI_1921",
#   KLK_FI_1922: "KLK_FI_1922",
#   KLK_FI_1923: "KLK_FI_1923",
#   KLK_FI_1924: "KLK_FI_1924",
#   KLK_FI_1925: "KLK_FI_1925",
#   KLK_FI_1926: "KLK_FI_1926",
#   KLK_FI_1927: "KLK_FI_1927",
#   KLK_FI_1928: "KLK_FI_1928",
#   KLK_FI_1929: "KLK_FI_1929",
#   KLK_FI_1930: "KLK_FI_1930",
#   KLK_FI_1931: "KLK_FI_1931",
#   KLK_FI_1932: "KLK_FI_1932",
#   KLK_FI_1933: "KLK_FI_1933",
#   KLK_FI_1934: "KLK_FI_1934",
#   KLK_FI_1935: "KLK_FI_1935",
#   KLK_FI_1936: "KLK_FI_1936",
#   KLK_FI_1937: "KLK_FI_1937",
#   KLK_FI_1938: "KLK_FI_1938",
#   KLK_FI_1939: "KLK_FI_1939",
#   KLK_FI_1940: "KLK_FI_1940",
#   KLK_FI_1941: "KLK_FI_1941",
#   KLK_FI_1942: "KLK_FI_1942",
#   KLK_FI_1943: "KLK_FI_1943",
#   KLK_FI_1944: "KLK_FI_1944",
#   KLK_FI_1945: "KLK_FI_1945",
#   KLK_FI_1946: "KLK_FI_1946",
#   KLK_FI_1947: "KLK_FI_1947",
#   KLK_FI_1948: "KLK_FI_1948",
#   KLK_FI_1949: "KLK_FI_1949",
#   KLK_FI_1950: "KLK_FI_1950",
#   KLK_FI_1951: "KLK_FI_1951",
#   KLK_FI_1952: "KLK_FI_1952",
#   KLK_FI_1953: "KLK_FI_1953",
#   KLK_FI_1954: "KLK_FI_1954",
#   KLK_FI_1955: "KLK_FI_1955",
#   KLK_FI_1956: "KLK_FI_1956",
#   KLK_FI_1957: "KLK_FI_1957",
#   KLK_FI_1958: "KLK_FI_1958",
#   KLK_FI_1959: "KLK_FI_1959",
#   KLK_FI_1960: "KLK_FI_1960",
#   KLK_FI_1961: "KLK_FI_1961",
#   KLK_FI_1962: "KLK_FI_1962",
#   KLK_FI_1963: "KLK_FI_1963",
#   KLK_FI_1964: "KLK_FI_1964",
#   KLK_FI_1965: "KLK_FI_1965",
#   KLK_FI_1966: "KLK_FI_1966",
#   KLK_FI_1967: "KLK_FI_1967",
#   KLK_FI_1968: "KLK_FI_1968",
#   KLK_FI_1969: "KLK_FI_1969",
#   KLK_FI_1970: "KLK_FI_1970",
#   KLK_FI_1971: "KLK_FI_1971",
#   KLK_FI_1972: "KLK_FI_1972",
#   KLK_FI_1973: "KLK_FI_1973",
#   KLK_FI_1974: "KLK_FI_1974",
#   KLK_FI_1975: "KLK_FI_1975",
#   KLK_FI_1976: "KLK_FI_1976",
#   KLK_FI_1977: "KLK_FI_1977",
#   KLK_FI_1978: "KLK_FI_1978",
#   KLK_FI_1979: "KLK_FI_1979",
#   KLK_FI_1980: "KLK_FI_1980",
#   KLK_FI_1981: "KLK_FI_1981",
#   KLK_FI_1982: "KLK_FI_1982",
#   KLK_FI_1983: "KLK_FI_1983",
#   KLK_FI_1984: "KLK_FI_1984",
#   KLK_FI_1985: "KLK_FI_1985",
#   KLK_FI_1986: "KLK_FI_1986",
#   KLK_FI_1987: "KLK_FI_1987",
#   KLK_FI_1988: "KLK_FI_1988",
#   KLK_FI_1989: "KLK_FI_1989",
#   KLK_FI_1990: "KLK_FI_1990",
#   KLK_FI_1991: "KLK_FI_1991",
#   KLK_FI_1992: "KLK_FI_1992",
#   KLK_FI_1993: "KLK_FI_1993",
#   KLK_FI_1994: "KLK_FI_1994",
#   KLK_FI_1995: "KLK_FI_1995",
#   KLK_FI_1996: "KLK_FI_1996",
#   KLK_FI_1997: "KLK_FI_1997",
#   KLK_FI_1998: "KLK_FI_1998",
#   KLK_FI_1999: "KLK_FI_1999",
#   KLK_FI_2000: "KLK_FI_2000"
# ] DEFAULT KLK_FI_1917
# PARAMETER OPTIONAL seed: "Random seed" TYPE INTEGER FROM 1000 TO 9999 (Use the same seed to repeat the same ordering of the results.)
# PARAMETER page: "Concordance page" TYPE INTEGER FROM 0 TO 9 DEFAULT 0 (Extract the specified page, 0-9, of up to 1000 results each, from the concordance.)
# RUNTIME python3

# This tool specifies attributes for a particular corpus.
# Omitted KLK_FI_2011 having different set of attributes.

import json, math, random

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_korp import parse_queries, request_kwic
import lib_names as names

# enforce *something* sensible because it seems all too easy to use a
# multimegabyte concordance file (*.json) as a "query" in Mylly GUI;
# query parser in lib_korp also tries to guard against nonsense in
# content by now
names.enforce('query.cqp.txt', '.cqp.txt')

seed = random.randrange(1000, 10000) if math.isnan(seed) else seed
names.output('result.korp.json',
             names.replace('query.cqp.txt',
                           '-s{}p{}.korp.json'.format(seed, page)))

comma = ','

CORPUS = corpus

ANNO = comma.join('''

	dephead deprel lemma lemmacomp lex msd nerbio nertag ocr pos
	ref word

'''.split())

META = comma.join('''

	paragraph paragraph_id sentence_id sentence_local_id
	sentence_parse_state text_binding_id text_datefrom text_dateto
	text_elec_date text_img_url text_issue_date text_issue_no
	text_issue_title text_label text_language text_page_id
	text_page_no text_part_name text_publ_id text_publ_part
	text_publ_title text_publ_type text_sentcount text_timefrom
	text_timeto text_tokencount

'''.split())

QUERIES = parse_queries('query.cqp.txt')

kwic = request_kwic(corpus = CORPUS,
                    seed = seed,
                    size = 1000,
                    page = page,
                    anno = ANNO,
                    meta = META,
                    queries = QUERIES)

# note: it *adds* dict(M = dict(origin = size * page)) to the kwic

with open('result.korp.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(kwic, result,
              ensure_ascii = False,
              check_circular = False)
