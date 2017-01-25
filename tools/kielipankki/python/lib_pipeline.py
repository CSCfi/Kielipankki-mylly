# Canned pipelines for any number of command types. Initially, one.

# These produce numbered error logs that the caller can then
# consolidate with lib_errorlog.consolidate(), q.v. Other input and output
# file names depend on the command type. Caller is expected to know.

# Attempting the following with input from a file, diagnostics to
# files, and output to a file. Not sure if binary mode are correct,
# whether the two processes really are properly waited for, and
# closing that stdout looks funny but maybe it really is that way.
# https://docs.python.org/3/library/subprocess.html#replacing-shell-pipeline

import os
from subprocess import Popen, PIPE

def hfst_lookup(*command):
    with Popen(["cut", "-f", "1"],
               stdin  = open("tokens.tsv", mode = "rb"),
               stdout = PIPE,
               stderr = open("error1.log", mode = "wb")) as cut:
        with Popen(command,
                   stdin = cut.stdout,
                   stdout = open("readings.txt", mode = "wb"),
                   stderr = open("error2.log", mode = "wb")) as process:
            cut.stdout.close()    # Allows cut to receive SIGPIPE?
            process.communicate() # stdout and stderr are in files now.

# "Processing" means tokenizing, looking up, then formatting.
# Something like that anyway.

def hfst_process(*command):
    with Popen(command,
               stdin  = open("text.txt", mode = "rb"),
               stdout = open("readings.txt", mode = "wb"),
               stderr = open("error.log", mode = "wb")) as process:
        pass

def hfst_process2(*command):
    with Popen(command,
               stdin  = open("text.txt", mode = "rb"),
               stdout = open("segments.txt", mode = "wb"),
               stderr = open("error.log", mode = "wb")) as process:
        pass

def aaltoasr(command):
    with Popen(command,
               stdout = open("error-out.txt", mode = "wb"),
               stderr = open("error.log", mode = "wb")) as process:
        pass

def iconv(*command):
    # command specifies input and output files, so there should not be
    # reading from stdin or writing to stdout, right?
    with Popen(command,
               stderr = open("error.log", mode = "wb")) as process:
        pass

def turku_parser_wrapper(wrapper):
    # It's a shell script, it expects to find its component things in
    # its current working directory, and it leaves things in TMPDIR.
    with Popen([wrapper],
               cwd = os.path.dirname(wrapper),
               env = dict(os.environ, TMPDIR = os.getcwd()),
               stdin  = open("text.txt", mode = "rb"),
               stdout = PIPE,
               stderr = open("error1.log", mode = "wb")) as parser:
        with Popen(["cut", "-f", "1,2,4,6,8,10,12"],
                   stdin = parser.stdout,
                   stdout = open("analyses.txt", mode = "wb"),
                   stderr = open("error2.log", mode = "wb")) as cut:
            pass
