import re
from itertools import chain, groupby

# Have screen(...) enforce that
# - non-empty lines start with a non-whitespace character
# - <-lines do not contain any tab character
# - <-lines are either <name </name or <!--
# - number of tabs on non-empty non-< lines is constant
# - <!-- Positional attributes: match number of tabs
# - <!-- Positional attributes: match each other

# This way positional
# - positional tab-separated fields are unambiguous
# - first field is always non-empty
# - each element tag have an unambiguous name
# - each hoisted line (tag, comment, or empty) is one field
# - hoisted lines are in known extra positions

class VeRTicalError(Exception): pass

def bad(line):
    '''Format offending line for a VeRTicalError message'''
    return '{}{}'.format(repr(line[:14]),
                         '...' if len(line) > 14 else '')

def ismeta(line):
    '''Not a token line'''
    return (line.startswith('<') or
            line.isspace() or
            line == '')

def ispositionals(line):
    '''Sigh.'''
    pattern = R'<!--\s*Positional\s+attributes\s*:\s*[\w\s]+-->\s*'
    return re.fullmatch(pattern, line)

def positionals(line):
    '''Return the string of space-separated positional attribute names
    from a special comment line.

    '''

    components = re.finditer(R'\w+', line)
    next(components) # "Positional" match object
    next(components) # "attributes" match object
    return ' '.join(m.group(0) for m in components) # the names

def ishoistable(line, hoistables):
    '''Return True if line is a hoistable meta line: a comment or space or
    empty or one of the hoistables.

    Except there is no space! (Unless just final newline?)
    '''

    return (line.startswith('<!--') or
            line.isspace() or
            line == '' or
            re.match(R'</?(\w+)', line).group(1) in hoistables)

# Intended usage:
# box = Positionals()
# ... hoisted(screen(source, box), hoisted_elements) ...
# posnames = box.names
# poscount = box.count
# where screen strips newlines and extracts names/field-count into box.
# What a crock, though.

class Positionals:
    
    def __init__(self):
        self.names = None
        self.count = None

    def check(self, k, line):
        # line without final newline already
        if line == '':
            pass
        elif re.match(R'\s', line):
            raise VeRTicalError('leading whitespace: line {}: {}'
                                .format(k, bad(line)))
        elif line.startswith('<!--'):
            self.checkcomment(k, line)
        elif line.startswith('<'):
            self.checkmarkup(k, line)
        else:
            self.checktoken(k, line)

    def checkcomment(self, k, line):
        if '\t' in line:
            raise VeRTicalError('tab in comment: line {}: {}'
                                .format(k, bad(line)))
        if ispositionals(line):
            names = positionals(line)
            if self.names is None:
                self.names = names
            elif self.names != names:
                raise VeRTicalError('conflicting names: line {}: {} =/= {}'
                                    .format(k, names, self.names))
            if self.count is None:
                self.count = names.count(' ') + 1
            elif self.count != names.count(' ') + 1:
                raise VeRTicalError('number of names differs '
                                    'from field count: '
                                    'line {}: {}: {}'
                                    .format(k, names, self.count))

    def checkmarkup(self, k, line):
        if '\t' in line:
            raise VeRTicalError('tab in tag: line {}: {}'
                                .format(k, bad(line)))
        if not re.match(R'</?[a-z]+[ >]', line):
            raise VeRTicalError('bad name in tag: line {}: {}'
                                .format(k, bad(line)))

    def checktoken(self, k, line):
        if self.count is None:
            self.count = line.count('\t') + 1
        elif self.count != line.count('\t') + 1:
            raise VeRTicalError('conflicting field count: line {}: {} =/= {}'
                                .format(k, line.count('\t') + 1, self.count))

def screen(source, box):

    '''Yield all content lines, stripped of their final newline, checked
    for such characteristics that would play havoc in undoing a hoist,
    with the side effect of storing in box the positional names and
    field count (if any).

    '''

    for k, line in enumerate(source, start = 1):
        line = line.rstrip('\n')
        box.check(k, line)
        yield line

def hoisted(source, elements):
    '''Yield all lines from VRT source with ignorable markup/comment
    groups hoisted upon the immediately following datum.

    The purpose is to remove ignorable markup that occurs internally
    to a sentence. Other ignorable markup can be safely left together
    with non-ignorable markup, as is.

    It is very important to note that final newlines must have been
    stripped from source.

    '''

    hoist = None
    for kind, group in groupby((line for line in source),
                               ismeta):
        items = list(group)
        if kind and all(ishoistable(item, elements)
                        for item in items):
            # meta lines, all hoistable
            hoist = items
            continue
        if hoist:
            # previous group was markup, current group is tokens
            # -- should check that no hoisted item contains a tab
            items[0] = '\t'.join(chain([items[0]], hoist))
            hoist = None
        yield from items
    else:
        if hoist:
            # source ended with all-hoistable markup lines
            yield from hoist

def sentences(source):
    '''Yield lists of consecutive "words" from VRT lines.

    A word is the first field (before a tab, if any) of a data line.

    '''

    def first(line):
        return re.match('[^\t\n]+', line).group()

    for meta, group in groupby(source, ismeta):
        if not meta:
            yield list(map(first, group))
