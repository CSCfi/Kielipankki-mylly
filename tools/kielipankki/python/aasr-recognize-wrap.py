# TOOL aasr-recognize-wrap.py: "Aalto ASR Recognize - Prepare Job" (Wraps an audio file for speech recognition in the batch system. Use the corresponding Run Job tool on the resulting wrap.)
# INPUT audio.wav TYPE GENERIC
# OUTPUT data.wrap
# OUTPUT OPTIONAL error.log
# PARAMETER Script TYPE [yes: "yes"] DEFAULT yes (Always output transcript in script.txt)
# PARAMETER SegWord TYPE [yes: "yes"] DEFAULT yes (Always output word level segmentation)
# PARAMETER SegMorph TYPE [yes: "yes", no: "no"] DEFAULT no (Optionally output morph level segmentation)
# PARAMETER SegPhone TYPE [yes: "yes", no: "no"] DEFAULT no (Optionally output phone level segmentation)
# PARAMETER RawTranscript TYPE [yes: "yes", no: "no"] DEFAULT no (Raw transcript format -- default is to postprocess)
# RUNTIME python3

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
import lib_wrap as wraps
import lib_names as names

# make ./data.wrap appear as $audio.wrap ISWIM
tag = "Aalto ASR Recognize Wrap"
names.output("./data.wrap", names.replace("audio.wav", ".wrap"))

mode = [ 'trans', 'segword' ]
if SegMorph == 'yes': mode.append('segmorph')
if SegPhone == 'yes': mode.append('segphone')
mode = ','.join(mode)

raw = "--raw" if RawTranscript == "yes" else ""

temp = R'''#! /bin/bash -e
#SBATCH -J mylly-aasr-rec
#SBATCH -o {{path}}/stdout.log
#SBATCH -e {{path}}/stderr.log
#SBATCH -p serial
#SBATCH -n 1
#SBATCH -t {time}
#SBATCH --mem-per-cpu={mem}

set -o pipefail

module load aaltoasr/1.1

aaltoasr-rec \
    --output {{path}}/script.txt \
    --tg {{path}}/script.textgrid \
    --elan {{path}}/script.eaf \
    --mode {mode} \
    {raw} \
    {{path}}/data/audio.wav

touch {{path}}/state/finished
'''

wraps.setup_wrap(tag, "./audio.wav")

# "./script.txt", "./script.textgrid", "./script.eaf"

wraps.setup_job(tag, temp.format(time = '2:00:00',
                                 mem = '16000',
                                 mode = mode,
                                 raw = raw))

# TODO: compute those parameters based on ./audio.data, some-how.
