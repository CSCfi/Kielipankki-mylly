# TOOL td-wrap.py: "Turku Dependency Wrap" (Wraps a text for parsing in the batch system. Use Turku Dependency Job on the resulting wrap.)
# INPUT text.txt TYPE GENERIC
# OUTPUT data.wrap
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import os
import tempfile
from zipfile import ZipFile

def wrap_text():
    '''
    Wraps ./text.txt in ./data.wrap

    Creates $WRKDIR/wrap<tmp>
    Creates $WRKDIR/wrap<tmp>/wrap.job

    ./data.wrap" is a zip archive file containing the following two items:

    - ticket/wrap<tmp> with "Turku Dependency Wrap" on first line
    - data/text.txt

    Another tool, td-job.py, is then used to run the wrapped job.
    '''

    path = tempfile.mkdtemp(prefix = 'wrap', dir = os.environ['WRKDIR'])
    name = os.path.basename(path)
    with ZipFile("data.wrap", "w") as wrap:
        # one is on Python 3.4
        # since Python 3.5 one could create new archive with mode "x"
        # since Python 3.6 one could open an archive member with mode "w"
        wrap.writestr("ticket/{}".format(name), "Turku Dependency Wrap\n")
        wrap.write("./text.txt", arcname = "data/text.txt")
        # that does not seem to compress text.txt - should one compress?

    make_job(path)

template_job = '''\
#! /bin/bash -e
#SBATCH -J mylly-td-parse
#SBATCH -o {path}/log-%J.out
#SBATCH -e {path}/log-%J.err
#SBATCH -p serial
#SBATCH -n 1
#SBATCH -t {time}
#SBATCH --mem-per-cpu={mem}

set -o pipefail

(
  cd /appl/ling/finnish-process/share/hfst/fi/Finnish-dep-parser-alpha

  export TMPDIR={path}

  # TODO: sanitize parser input

  ./parser_wrapper.sh < {path}/data/text.txt |
  cut -f 1,2,4,6,8,10,12 > {path}/analyses.txt
)

touch {path}/state/finished
'''

def make_job(path):
    '''Make path/wrap.job, to be submitted to a batch queue'''

    with open(os.path.join(path, "wrap.job"), "w") as job:
        print(template_job
              .format(path = path,
                      time = '2:00:00', # needs computed from text.txt
                      mem = '16000'),   # needs computed from text.txt
              file = job)

wrap_text()

# consolidate() any error logs the user should see, if any
