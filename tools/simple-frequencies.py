#! /usr/bin/env python3

# Reads ./input.txt (running UTF-8 text, reads maxlines + 1 lines)
# Writes ./output.txt (frequencies of maximal "word-character" sequences)

# This script is a toy, useful for learning Chipster. This script
# could be parameterized for the number of tokens (including tied
# tokens or not), or a threshold frequency (to learn to allow
# parameters). - A family of scripts like this is sufficient to build
# workflows: tokenize like this OR use a better tokenizer OR parse to
# get best tokens with lemmas and maybe filter undesired tokens out,
# maybe select a column from parser output and THEN count frequencies
# with another script like this that reads tokens, one on each line.
# Maybe summarize frequency distribution (like, 5 or 11 order
# statistics). (Also, people will want character encoding guessers and
# mappers, with mind-reading ability. And sarcasm detectors.)

import collections, re

token = re.compile(r'\w+')

def tokens(source, maxlines = 1000):
    for k, line in enumerate(source):
        if k == maxlines:
            return
        for t in token.findall(line):
            yield t

def readlines():
    with open('input.txt', encoding = 'utf-8') as o:
        return collections.Counter(tokens(o, 1000))

def writefrequencies(counts):
    with open('output.txt', mode = 'w', encoding = 'utf-8') as o:
        for t, f in counts.most_common():
            print('{:>6}\t{}'.format(f, t), file = o)

if __name__ == '__main__':
    writefrequencies(readlines())
