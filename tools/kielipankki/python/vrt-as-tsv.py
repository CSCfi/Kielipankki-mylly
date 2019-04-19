# TOOL vrt-as-tsv.py: "VRT as Rel.TSV" (Write data and meta relations that represent standard VRT content - tokens within text, paragraph, sentence elements - and a summary report)
# INPUT data.vrt TYPE GENERIC
# OUTPUT data.tsv
# OUTPUT info.txt
# OUTPUT OPTIONAL sentence-meta.tsv
# OUTPUT OPTIONAL paragraph-meta.tsv
# OUTPUT OPTIONAL text-meta.tsv
# RUNTIME python3

import os, sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name

own = base('data.vrt', '*.vrt.txt')
name('data.tsv', own, ins = 'data', ext = 'rel.tsv')
name('info.txt', own, ins = 'info', ext = 'txt')
name('sentence-meta.tsv', own, ins = 'sentence-meta', ext = 'rel.tsv')
name('paragraph-meta.tsv', own, ins = 'paragraph-meta', ext = 'rel.tsv')
name('text-meta.tsv', own, ins = 'text-meta', ext = 'rel.tsv')

# An error if there are no tokens *and* no head - cannot produce an
# empty relation without a single example of what the head should be -
# but *all* three meta files are optional! if no such element was ever
# encountered, there is no such file and no need to magick attribute
# names out of nowhere.

# Standard structure as meta, sentences/tokens as data, with 1-based
# counters, using provided positional names if provided in a comment,
# uniquely, and matching record length, else using V1, ...

import html, re
from collections import Counter
from itertools import groupby
from operator import itemgetter

# ignored start and end tags and comments must not break token runs so
# standard does not yield anything on them, only keeps these counts
# for info
igopencounts = Counter()
igclosecounts = Counter() # element only
igkeycounts = Counter() # attribute name only
emptycount = 0
headcounts = Counter() # from comments that set positional head
commentcount = 0 # any other comment
headline = None # set on first token or from such comment

# these characters do not occur in the input, not even as entities, so
# this translation is a no-op and can do no harm (need to add some
# more such characters)
nop = str.maketrans(dict((c, '?') for c in '\t\n'))

def unescape(item):
    return html.unescape(item).translate(nop)

def meta(line):
    name, = re.findall('^<(\w+)', line)
    it = dict(('{}_{}'.format(name, key), unescape(value))
              for key, value
              in re.findall('(\w+)\s*=\s*"([^"]*)"', line))
    return name, it

def end(line):
    name, = re.findall('^</(\w+)>', line)
    return name

def data(line):
    record = tuple(map(unescape, line.rstrip('\n').split('\t')))
    return record

def standard(lines, out):
    global headline # may be set in transform if token is first
    global commentcount
    global emptycount
    for line in lines:
        if line.isspace():
            # so empty lines are allowed and ignored
            emptycount += 1
        elif line.startswith('<!-- #vrt positional-attributes:'):
            # e.g., <!-- #vrt positional-attributes: word -->
            com, ment = line.split(':', 1)
            names = tuple(re.findall('[\w.-]+', ment))
            if len(set(names)) < len(names):
                # not positional attributes after all
                commentcount += 1
            else:
                headcounts[names] += 1
                if headline is None:
                    headline = names
                    print('kMtext', 'kMparagraph', 'kMsentence', 'kMtok',
                          *headline,
                          sep = '\t', file = out)
        elif line.startswith('<!--'):
            commentcount += 1
        elif line.startswith(('<text ', '<text>',
                              '<paragraph ', '<paragraph>',
                              '<sentence ', '<sentence>')):
            name, it = meta(line)
            yield 'push', name, it
        elif line.startswith(('</sentence>',
                              '</paragraph>',
                              '</text>')):
            yield 'pop', end(line)
        elif line.startswith(('</')):
            igclosecounts[name] += 1
            # ignored but also reported as such
        elif line.startswith('<'):
            name, it = meta(line)
            igopencounts[name] += 1
            for key in it: igkeycounts[key] += 1
            # ignored but also reported as such
        else:
            yield 'data', data(line)

def transform(lines, out, info, outs):
    global headline # may be set in standard if there are comments
    namestack, metastack = [], []
    current = Counter(text = 0, paragraph = 0, sentence = 0)
    mispopcounts = Counter() # ...
    keys = dict(text = None, paragraph = None, sentence = None)
    opencounts = Counter() # namestack at each push
    closecounts = Counter() # namestack at each pop
    keycounts = dict(text = Counter(), # each key observation
                     paragraph = Counter(), # oops could be one Counter
                     sentence = Counter())  # because names are in keys
    fieldcounts = Counter()
    tok = 0 # reset at any sentence, step at any token
    orphan = 0 # step at any token outside sentence
    for kind, group in groupby(standard(lines, out),
                               key = itemgetter(0)):
        if kind == 'push':
            for _, name, it in group:
                namestack.append(name)
                metastack.append(it)
                opencounts['/'.join(namestack)] += 1
                current[name] += 1
                if keys[name] is None: # first encounter of name
                    keys[name] = sorted(it)
                    print('kM{}'.format(name),
                          *keys[name],
                          sep = '\t', file = outs[name])
                print(current[name],
                      *(it.get(key, '_') for key in keys[name]),
                      sep = '\t', file = outs[name])
                for key in it: keycounts[name][key] += 1
                if name == 'sentence': tok = 0
        elif kind == 'pop':
            for _, name in group:
                closecounts['/'.join(namestack)] += 1
                if not namestack or namestack[-1] != name:
                    mispopcounts['/'.join(namestack), name] += 1
                # please do not crash because info at end
                namestack and namestack.pop()
                metastack and metastack.pop()
        elif kind == 'data':
            # continue current sentence, or orphan outside sentence,
            # so that sentence and token counter together identify
            # token -- Python has loop variable in function scope
            if 'sentence' not in namestack: tok = orphan
            for tok, item in enumerate(group, start = tok + 1):
                _, record = item
                fieldcounts[len(record)] += 1
                if headline is None: # first encounter precedes comment
                    headline = tuple('V{}'.format(k)
                                     for k, _ in enumerate(record, start = 1))
                    print('kMtext', 'kMparagraph' ,'kMsentence', 'kMtok',
                          *headline,
                          sep = '\t', file = out)
                if len(record) != len(headline):
                    # cut or pad to size -- this should never happen
                    values = iter(record)
                    record = tuple(next(values, '_') for _ in headline)
                print(current['text'] if 'text' in namestack else 0,
                      current['paragraph'] if 'paragraph' in namestack else 0,
                      current['sentence'] if 'sentence' in namestack else 0,
                      tok, *record, sep = '\t', file = out)
            if 'sentence' not in namestack: orphan = tok
        else:
            # program error
            raise Exception('unexpected kind: {}'.format(kind))
    else:
        # after processing every line, produce also a report
        
        if headline is None:
            # without head cannot produce even empty relation
            print('No token and no positional names found',
                  file = sys.stderr)
            exit(1)
        
        if namestack: print('Element open at end:', '/'.join(namestack),
                            sep = '\n', end = '\n\n', file = info)

        print('Counts of elements opened (closed):', file = info)
        for name in opencounts:
            print('{} ({})\t{}'.format(opencounts[name],
                                       closecounts[name],
                                       name),
                  file = info)
        else: print(file = info)

        if set(closecounts) - set(opencounts):
            print('Counts of elements not opened yet closed:', file = info)
            for name in closecounts:
                if name in opencounts: continue
                print(closecounts[name], name, sep = '\t', file = info)
            else: print(file = info)

        if mispopcounts:
            print('Counts of elements closed out of order:', file = info)
            for element, name in sorted(mispopcounts):
                print(mispopcounts[element, name],
                      # the / disconcerts less than (ISWIM)
                      '{} ended as {}'.format(element or '/', name),
                      sep = '\t', file = info)
            else: print(file = info)

        flag = False
        print('Counts of structural attributes seen:', file = info)
        for name in sorted(keycounts): # oops redundant level
            for key in sorted(keycounts[name]):
                if key in keys[name]: # or maybe not redundant
                    print(keycounts[name][key], '{} {}'.format(name, key),
                          sep = '\t', file = info)
                else:
                    flag = True
                    print(keycounts[name][key], '{} *{}'.format(name, key),
                          sep = '\t', file = info)
        else:
            if flag:
                print('(*omitted because not first)', file = info)
            else:
                print(file = info)

        if headcounts:
            print('Counts of positional attribute names seen:',
                  file = info)
            for head in sorted(headcounts):
                print(headcounts[head], ' '.join(head),
                      sep = '\t', file = info)
            else: print(file = info)
        
        print('Positional attribute names used - Vk if token first:',
              file = info)
        print(' '.join(headline), file = info)
        print(file = info)

        if commentcount:
            print(('{} comment' if commentcount == 1 else '{} comments')
                  .format(commentcount), 'ignored',
                  file = info)
            print(file = info)

        if emptycount:
            print('Ignored',
                  ('{} empty line' if emptycount == 1 else '{} empty lines')
                  .format(emptycount),
                  file = info)
            print(file = info)

        if fieldcounts:
            print('Counts of seen token-record lengths:', file = info)
            for n in sorted(fieldcounts):
                print(fieldcounts[n],
                      ('{} field' if n == 1 else '{} fields').format(n),
                      sep = '\t', file = info)
            else: print(file = info)

        if igopencounts or igclosecounts:
            print('Counts of ignored elements opened (closed):',
                  file = info)
            for name in sorted(set(igopencounts) |
                               set(igclosecounts)):
                print('{} ({})'.format(igopencounts[name],
                                       igclosecounts[name]),
                      name, sep = '\t', file = info)
            else: print(file = info)

        if igkeycounts:
            print('Counts of ignored structural attributes seen:',
                  file = info)
            for key in sorted(igkeycounts):
                print(igkeycounts[key], key, sep = '\t', file = info)
            else: print(file = info)

def main():
    with open('data.vrt', encoding = 'UTF-8') as source, \
         open('data.tmp', mode = 'w', encoding = 'UTF-8') as data, \
         open('info.tmp', mode = 'w', encoding = 'UTF-8') as info, \
         open('sent.tmp', mode = 'w', encoding = 'UTF-8') as sent, \
         open('para.tmp', mode = 'w', encoding = 'UTF-8') as para, \
         open('text.tmp', mode = 'w', encoding = 'UTF-8') as text:
        
        transform(source, data, info,
                  dict(text = text,
                       paragraph = para,
                       sentence = sent))

    os.rename('data.tmp', 'data.tsv')

    os.rename('info.tmp', 'info.txt')

    if os.path.getsize('sent.tmp'):
        os.rename('sent.tmp', 'sentence-meta.tsv')

    if os.path.getsize('para.tmp'):
        os.rename('para.tmp', 'paragraph-meta.tsv')

    if os.path.getsize('text.tmp'):
        os.rename('text.tmp', 'text-meta.tsv')

main()
