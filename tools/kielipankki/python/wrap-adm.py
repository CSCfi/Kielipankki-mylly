# TOOL wrap-adm.py: "Admin tool" (Attend to extant work directories of batch jobs, if appropriately informed and so inclined.)
# OUTPUT info.log
# OUTPUT OPTIONAL error.log
# PARAMETER Secret TYPE STRING DEFAULT "" (Must know something)
# PARAMETER Ticket TYPE STRING DEFAULT "ignored" (Aka directory name)
# PARAMETER Action TYPE [info: "info", env: "Show some environment variables", remove: "Remove ticket work directory"] DEFAULT info ()

import hashlib

h = hashlib.sha256()
h.update(Secret.encode('UTF-8'))

with open('info.log', 'w') as info:

    if h.hexdigest() == ( 'f0630e2bac6e41a4'
                          'b6daae1b394a8eaa'
                          '4e62679703cc6522'
                          '9d78fb57c1ed2e31' ):

        sys.path.append(os.path.join(chipster_module_path, "python"))
        from lib_wrap_adm import dispatch
        dispatch(info, Action, Ticket)

    else:

        print('Sorry must know a secret',
              file = info)
