import os

from subprocess import Popen, PIPE
from io import TextIOWrapper

def formatkeys(head, keys):
    return [
        '--key={key},{key}{kind}{sign}'
        .format(key = head.index(attr) + 1,
                kind = ( 'n' if kind == 'integer' else
                         'g' if kind == 'float' else
                         '' if kind == 'string' else # 'default'
                         'n' if attr.startswith(('kM', 'cM')) else
                         'g' if attr.startswith(('uM', 'wM')) else
                         '' ),
                sign = ( '' if sign == 'increasing' else # 'decreasing'
                         'r' ))
        for attr, kind, sign in keys
    ]

# the following do not really need a relation file any more, any TSV
# will be fine; maybe there should also be an option to not be stable
# when there are keys?

def process(relationfile, process, *keys):
    process1(relationfile, process, False, *keys)

def processanyway(relationfile, process):
    '''No keys but sort anyway, for uniqueness. Needs a better name.'''
    process1(relationfile, process, True)

def process1(relationfile, process, anyway, *keys):
    '''In which a relation may be on the physically large side, so an
    external sort that is engineered to cope with such is used.

    Keys are triples of (attr, kind, sign) where attr is an attribute
    name, kind indicates default, integer, float, string type, and
    sign is either increasing or decreasing. Default type is numeric
    when indicated by a Mylly prefix. Explicit kind overrides.

    With zero keys, do not sort: data is already in *that* order.
    (Update: now can be asked to sort anyway, to support counting and
    making relations out of more general TSV.)

    '''
    
    with open(relationfile, mode = 'rb', buffering = 0) as source:
        
        head = next(source).decode('UTF-8').rstrip('\n').split('\t')
        keyx = formatkeys(head, keys)

        # with no keys, do not sort (merge of one is just a copy)
        # unless specifically asked to sort anyway
        if not keyx and not anyway: keyx = [ '--merge' ]

        # without locale control, appeared to sort case-insensitive
        # which is not right when the purpose is to group by identity
        # as string
        
        with Popen(['sort', '--stable', '--field-separator=\t'] + keyx,
                   env = dict(os.environ, LC_ALL = 'C'),
                   stdin = source,
                   stdout = PIPE) as sort:
            process(TextIOWrapper(sort.stdout, encoding = 'UTF-8'))

        # still unsure of this part
        # sort.communicate(timeout = 3)
        if sort.returncode is None:
            sort.kill()
            sort.communicate()
            exit(11)
        elif sort.returncode:
            raise Exception('sort returned with {}'
                            .format(sort.returncode))

def save(relationfile, resultfile, *keys):
    save1(relationfile, resultfile, False, *keys)

def saveanyway(relationfile, resultfile):
    '''Needs a better name. But is this even needed for anything?'''
    save1(relationfile, resultfile, True)

def save1(relationfile, resultfile, anyway, *keys):
    '''Writes the sorted result straight out.

    Update: allow sorting anyway when no keys provided, as in the
    piping variant above, though not sure of a use case.

    '''

    with open(relationfile, mode = 'rb', buffering = 0) as source, \
         open(resultfile, mode = 'wb') as target:

        binhead = next(source)
        target.write(binhead)
        target.flush()

        head = binhead.decode('UTF-8').rstrip('\n').split('\t')
        keyx = formatkeys(head, keys)

        if not keyx and not anyway: keyx = [ '--merge' ]

        # without locale control, expected decimal separator to be a
        # comma, would not interpret decimal part after period
        
        with Popen(['sort', '--stable', '--field-separator=\t'] + keyx,
                   env = dict(os.environ, LC_ALL = 'C'),
                   stdin = source,
                   stdout = target) as sort:
            pass # wait

        # still unsure of this part
        # sort.communicate(timeout = 3)
        if sort.returncode is None:
            sort.kill()
            sort.communicate()
            exit(11)
        elif sort.returncode:
            raise Exception('sort returned with {}'
                            .format(sort.returncode))
