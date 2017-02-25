import os

def prepend_to_path(path, *entries):
    os.environ[path] = ( ':'.join((':'.join(entries),
                                   os.environ[path]))
                         .rstrip(':') )

def setenv(hfst_version):
    if hfst_version == 'v_3_12_1':
        prepend_to_path('PATH',
                        '/homeappl/appl_taito/ling/hfst/3.12.1/bin')
        prepend_to_path('LD_LIBRARY_PATH',
                        '/homeappl/appl_taito/ling/hfst/3.12.1/lib')
    else:
        # find out what is needed for summary v3121, then work on other
        # versions and other HFST programs
        pass
