from subprocess import Popen, PIPE
from io import TextIOWrapper

def process(relationfile, process, *keys):
    '''In which a relation may be on the physically large side, so an
    external sort that is engineered to cope with such is used.

    Sort numerically when indicated by a Mylly prefix.

    With zero keys, do not sort: data is already in *that* order.

    '''
    
    with open(relationfile, mode = 'rb', buffering = 0) as source:
        
        head = next(source).decode('UTF-8').rstrip('\n').split('\t')
        keyx = [
            '--key={key},{key}{how}'
            .format(key = head.index(key) + 1,
                    how = ( 'n' if key.startswith(('kM', 'cM')) else
                            'g' if key.startswith('wM') else
                            '' ))
            for key in keys
        ]

        if not keyx: keyx = [ '--merge' ] # do not sort

        # may also need to control locale or something - must, really,
        # so this will change (now it appears to sort case-insensitive
        # which is not right when the purpose is to group by identity
        # as string)
        
        with Popen(['sort', '--stable', '--field-separator=\t'] + keyx,
                   stdin = source,
                   stdout = PIPE,
                   stderr = open('errors.log', mode = 'wb')) as sort:

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
    '''Writes the sorted result straight out.

    '''
    
    with open(relationfile, mode = 'rb', buffering = 0) as source, \
         open(resultfile, mode = 'wb') as target:
        
        binhead = next(source)
        target.write(binhead)
        target.flush()
        
        head = binhead.decode('UTF-8').rstrip('\n').split('\t')
        keyx = [
            '--key={key},{key}{how}'
            .format(key = head.index(key) + 1,
                    how = ( 'n' if key.startswith(('kM', 'cM')) else
                            'g' if key.startswith('wM') else
                            '' ))
            for key in keys
        ]

        if not keyx: keyx = [ '--merge' ] # do not sort
        
        # may also need to control locale or something - or not? this
        # is properly just a backend to tsv-sort.py, not to be relied
        # on in further processing
        
        with Popen(['sort', '--stable', '--field-separator=\t'] + keyx,
                   stdin = source,
                   stdout = target,
                   stderr = open('errors.log', mode = 'wb')) as sort:
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
