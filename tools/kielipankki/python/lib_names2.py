import os, sys
from fnmatch import fnmatch

# https://github.com/chipster/chipster/wiki/TechnicalManual#output-file-names

# Usage in a Mylly tool script: enforce that an input display name
# matches a pattern, and base output display name on the first
# component of input name:
#
# base('input.ext', '*.foo.bar')
#   => 'ensin' if input.ext is like 'ensin.jotain-jotain.foo.bar'
#      in chipster-inputs.tsv
#   => error message otherwise
#
# name('output.ext', base('input.ext', '*'), ins = '1', ext = 'svg')
#   maps input.ext => ensin in chipster-inputs.tsv
#   to output.ext => ensin.1.svg in chipster-outputs.tsv
#   (ins and ext are keyword only, ins is optional)
#
# name('output.ext', 'constant', ext = 'svg')
#   maps output.ext => constant.svg in chipster-outputs.tsv

cash = None

def base(argname, *patterns):
    '''Enforces that there is a corresponding input
    name in chipster_inputs.tsv, it matches a
    pattern, and it has a first component.

    Returns the first component of the input
    name.

    '''

    global cash
    if cash is None:
        try:
            with open('chipster-inputs.tsv', 'r',
                      encoding = 'UTF-8') as chipsterin:
                cash = dict(record.strip('\r\n').split('\t')[:2]
                            for record in chipsterin
                            if not record.startswith('#'))
        except FileNotFoundError:
            print('chipster-inputs.tsv not found', file = sys.stderr)
            print('(this cannot happen - please report)', file = sys.stderr)
            exit(1)
        except ValueError:
            print('chipster-inputs.tsv could not be read', file = sys.stderr)
            print('(this cannot happen - please report)', file = sys.stderr)
            exit(1)

    if argname not in cash:
        print('input name', argname, 'not in chipster-inputs.tsv',
              file = sys.stderr)
        print('(this cannot happen - please report)', file = sys.stderr)
        exit(1)
    
    name = cash[argname]
    for pattern in patterns:
        if fnmatch(name, pattern):
            base = name.split('.', 1)[0]
            break
        else:
            continue
    else:
        print('input file name:', name, file = sys.stderr)
        print('does not match:', ', '.join(patterns), file = sys.stderr)
        exit(1)

    if not base:
        # not sure if this can even happen in Chipster
        print('input file name:', name, file = sys.stderr)
        print('has empty base part', file = sys.stderr)
        exit(1)

    return base

def name(resname, base, *, ext, ins = None):
    # to append to chipster_outputs.tsv
    try:
        with open('chipster-outputs.tsv', 'a', encoding = 'UTF-8') as out:
            print(resname, '.'.join((base, ins, ext) if ins else (base, ext)),
                  sep = '\t',
                  file = out)
    except Exception:
        print('could not append {} to chipster-outputs.tsv'
              .format(resname), file = sys.stderr)
        print('(this cannot happen - please report)', file = sys.stderr)
        exit(1)
