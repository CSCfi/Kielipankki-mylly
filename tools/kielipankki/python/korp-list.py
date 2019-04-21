# TOOL korp-list.py: "Corpus list"
# (Get a list of corpora from korp.csc.fi)
# OUTPUT korp.list.json
# OUTPUT korp.list.tsv
# RUNTIME python3

import json, os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_korp import request_list

info = request_list()

with open('korp.list.json', mode = 'w', encoding = 'utf-8') as result:
    json.dump(info, result,
              ensure_ascii = False,
              check_circular = False)

with open('korp.list.tsv', mode = 'w', encoding = 'utf-8') as out:
    print('protected', 'corpus', sep = '\t', file = out)
    protected = info['protected_corpora']
    for corpus in info['corpora']:
        print("ny"[corpus in protected], corpus, sep = '\t', file = out)
