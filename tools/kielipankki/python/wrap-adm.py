# TOOL wrap-adm.py: "Wrap Admin Tool" (Look at extant wrap work dirs, if appropriately informed and so inclined.)
# PARAMETER Secret: "This is nothing" TYPE STRING (Must know something)
# OUTPUT info.log
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import hashlib

h = hashlib.sha256()
h.update(Secret.encode('UTF-8'))

with open('info.log', 'w') as info:

    if h.hexdigest() == ( '618f2289a012bf19'
                          '84cee5f656abc077'
                          'f884b31dd77f3920'
                          '9e918a78ecf9f927' ):

        sys.path.append(os.path.join(chipster_module_path, "python"))
        import lib_wrap_adm
        lib_wrap_adm.print_info(info)

    else:

        print('That also is nothing',
              file = info)
