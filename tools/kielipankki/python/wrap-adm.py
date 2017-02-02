# TOOL wrap-adm.py: "Wrap Admin Tool" (Look at extant wrap work dirs, if appropriately informed and so inclined.)
# OUTPUT info.log
# OUTPUT OPTIONAL error.log
# PARAMETER Secret: "" TYPE STRING DEFAULT "This is nothing" (Must know something)
# RUNTIME python3

import hashlib

h = hashlib.sha256()
h.update(Secret.encode('UTF-8'))

with open('info.log', 'w') as info:

    if h.hexdigest() == ( 'f0630e2bac6e41a4'
                          'b6daae1b394a8eaa'
                          '4e62679703cc6522'
                          '9d78fb57c1ed2e31' ):

        sys.path.append(os.path.join(chipster_module_path, "python"))
        import lib_wrap_adm
        lib_wrap_adm.print_info(info)

    else:

        print('Sorry',
              file = info)
