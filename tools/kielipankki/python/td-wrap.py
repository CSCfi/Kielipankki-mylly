# TOOL td-wrap.py: "Turku Dependency Parser for Finnish - Prepare Job" (Prepares a text for parsing in the batch system. Use the corresponding Run Job on the resulting job.)
# INPUT text.txt TYPE GENERIC
# OUTPUT data.job
# OUTPUT OPTIONAL error.log
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_wraps as wraps
import lib_names as names

names.output("data.job", names.replace("text.txt", ".job"))

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

tag = "Turku Dependency Wrap"
wrapname = "data.job"

wraps.setup_wrap(wrapname, tag, "./text.txt")

wraps.setup_job(wrapname, tag,
                temp.format(time = '2:00:00',
                            mem = '16000'))

# TODO: compute those parameters based on ./text.txt, some-how.
