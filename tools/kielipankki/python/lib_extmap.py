import sys
from itertools import chain

def index(head, names): return tuple(map(head.index, names))
def value(record, ks): return tuple(record[k] for k in ks)

def scan(inf, source, hi, lo, keys):
    with open(inf, encoding = 'UTF-8') as ins:
        head = next(ins).rstrip('\n').split('\t')
        k = head.index(source)
        if not keys:
            keys = set(key
                       for line in ins
                       for it in [line.rstrip('\n').split('\t')[k]]
                       if it not in ('_', '')
                       for key, val in ( kv.split(lo, 1)
                                         for kv in it.split(hi) ))
            keys = tuple(sorted(keys))

    if set(keys) & set(head):
        print('conflicting names:', *sorted(set(keys) & set(head)),
              sep = '\n',
              file = sys.stderr)
        exit(1)

    return keys

def extend(inf, ouf, source, hi, lo, keys):
    with open(ouf, mode = 'w', encoding = 'UTF-8') as ous:
        with open(inf, mode = 'r', encoding = 'UTF-8') as ins:
            head = next(ins).rstrip('\n').split('\t')
            print(*chain(keys, head), sep = '\t', file = ous)
            k = head.index(source)
            for line in ins:
                record = line.rstrip('\n').split('\t')
                new = dict(pair
                           for it in [record[k]]
                           if it not in ('_', '')
                           for pair in ( kv.split(lo, 1)
                                         for kv in it.split(hi) ))
                print(*chain((new.get(key, '_') for key in keys),
                             record),
                      sep = '\t',
                      file = ous)
