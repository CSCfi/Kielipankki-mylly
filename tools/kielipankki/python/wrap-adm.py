# TOOL wrap-adm.py: "Wrap Admin Tool" (Look at extant wrap work dirs, if appropriately informed and so inclined.)
# OUTPUT info.log
# OUTPUT OPTIONAL error.log
# PARAMETER Secret: "" TYPE STRING DEFAULT "This is nothing" (Must know something)
# RUNTIME python3

import hashlib

h = hashlib.sha256()
h.update(Secret.encode('UTF-8'))

with open('info.log', 'w') as info:

    if h.hexdigest() == ( 'feccf7af59e54dbd'
                          '5e1092c5e6c0ff4b'
                          '38237c82554466ee'
                          '4619239545d29067' ):

        sys.path.append(os.path.join(chipster_module_path, "python"))
        import lib_wrap_adm
        lib_wrap_adm.print_info(info)

    else:

        print('Sorry',
              file = info)
