# TOOL to-utf8.py: "Convert to UTF-8" (Convert text from another character encoding)
# INPUT data.txt TYPE GENERIC
# OUTPUT text.txt
# OUTPUT OPTIONAL error.log
# PARAMETER Encoding TYPE [windows_1252: "Windows-1252"] DEFAULT windows_1252 (Input encoding)
# PARAMETER Handle TYPE [omit: "Omit", replace: "Replace"] DEFAULT omit (Omit or replace invalid data)
# PARAMETER Quiet TYPE [yes: "yes", no: "no"] DEFAULT no (Be quiet about problems)

import os
import sys

sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_pipeline import iconv
from lib_errorlog import consolidate

# iconv (GNU libc) 2.12

command = ["iconv", "--output", "text.txt"]

command.extend(("--from-code",
                "{}//{}".format(dict(windows_1252 = "WINDOWS-1252")
                                [Encoding],
                                dict(omit = "IGNORE",
                                     replace = "TRANSLIT")[Handle])))

command.extend(("--to-code", "UTF-8"))

if Quiet == "yes":
    command.append("-c")

command.append("data.txt") # input file

iconv(*command)

consolidate()
