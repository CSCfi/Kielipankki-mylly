# TOOL tsv-join.py: "Join TSV files"
# (Relational join of two TSV files)
# INPUT one.tsv TYPE GENERIC
# INPUT two.tsv TYPE GENERIC
# OUTPUT join.tsv
# RUNTIME python3

from collections import defaultdict
from itertools import chain

sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_names as names

names.output('join.tsv', names.replace('one.tsv', '-j.tsv'))

def index(head, names): return tuple(map(head.index, names))
def share(head, head2): return tuple(set(head) & set(head2))
def other(head, names): return tuple(set(head) - set(names))
def value(record, ks): return tuple(record[k] for k in ks)

def indices(head, head2):
    shared = share(head, head2)
    left, rite = other(head, shared), other(head2, shared)
    return (index(head, shared), index(head, left),
            index(head2, shared), index(head2, rite))

def read(source, com, oth):
    result = defaultdict(list)
    for line in source:
        record = line.rstrip('\n').split('\t')
        result[value(record, com)].append(value(record, oth))
    return result

# to do: could as easily read in only one of the files - the smaller
# one, most likely - then stream through the other file.

with open('one.tsv', encoding = 'utf-8') as fin1:
    with open('two.tsv', encoding = 'utf-8') as fin2:
        onehead = next(fin1).rstrip('\n').split('\t')
        twohead = next(fin2).rstrip('\n').split('\t')
        com1, oth1, com2, oth2 = indices(onehead, twohead)
        one = read(fin1, com1, oth1)
        two = read(fin2, com2, oth2)
        with open('join.tsv', mode = 'w', encoding = 'utf-8') as out:
            print(*chain(value(onehead, com1),
                         value(onehead, oth1),
                         value(twohead, oth2)),
                  sep = '\t',
                  file = out)
            for common, middle in one.items():
                for tail in two.get(common, ()):
                    for mid in middle:
                        print(*chain(common,
                                     mid,
                                     tail),
                              sep = '\t',
                              file = out)
