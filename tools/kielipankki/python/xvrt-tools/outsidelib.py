import os

MARMOTJAR = '/proj/kieli/varpunen/marmot-2014-10-22.jar'

MARMOTMODEL = '/proj/kieli/varpunen/models/fin_model.marmot'

UDPIPE = '/appl/ling/udpipe/1.2.0/bin/udpipe'

UDPIPEMODEL = (
    '/appl/ling/udpipe/models/udpipe-ud-2.3-181115/{}-2.3-181115.udpipe'
)

# certain scripts need HFSTBIN in PATH, and they need to work on
# certain servers that do not have HFSTBIN in PATH; and then those
# binaries need HFSTLIB in LD_LIBRARY_PATH, of course
HFSTBIN = '/appl/ling/hfst/3.15.0/bin'
HFSTLIB = '/appl/ling/hfst/3.15.0/lib'

HFSTTOKENIZE = '/appl/ling/hfst/3.15.0/bin/hfst-tokenize'
OMORFITOKENIZE = (
    '/appl/ling/finnish-tagtools/1.3.2/share/finnish-tagtools'
    '/omorfi_tokenize.pmatch'
)

FINER = (
    '/appl/ling/finnish-tagtools/1.3.2/bin/finnish-nertag'
)

FINPOS =  (
    '/appl/ling/finnish-tagtools/1.3.2/bin/finnish-postag'
)

def prepend(*paths, to):
    '''Prepend paths to the value of a environment variable.'''
    
    if to not in ('PATH', 'LD_LIBRARY_PATH'):
        raise Exception('unexpected path variable')

    old = os.environ.get(to)
    return ':'.join(paths + ((old,) if old else ()))
