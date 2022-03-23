# TOOL td-submit.py: "Turku Dependency Parser for Finnish - Submit Job" (Submits a text for parsing in the batch system. "Wait" for the results using the corresponding wait tool on the job file.)
# INPUT text.txt TYPE GENERIC
# OUTPUT generic.job
# OUTPUT OPTIONAL error.log

import os
import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_jobs as jobs
import lib_names as names

names.output('generic.job', names.replace('text.txt', '.job'))

temp = '''\
#! /bin/bash -e
#SBATCH -J mylly-td-parse
#SBATCH -o {{path}}/log-%J.out
#SBATCH -e {{path}}/log-%J.err
#SBATCH -p serial
#SBATCH -n 1
#SBATCH -t {time}
#SBATCH --mem-per-cpu={mem}

set -o pipefail

(
  cd /appl/ling/finnish-process/share/hfst/fi/Finnish-dep-parser-alpha

  export TMPDIR={{path}}

  # TODO: in place of that cat, sanitize parser input

  cat < {{path}}/data/text.txt |
  ./parser_wrapper.sh |
  cut -f 1,2,4,6,8,10,12 > {{path}}/analyses.txt
)

touch {{path}}/state/finished
'''

jobs.submit('generic.job', 'Turku Dependency Job',
            temp.format(time = '2:00:00',
                        mem = '16000'),
            'text.txt')

# TODO: compute those parameters based on ./text.txt, some-how.
