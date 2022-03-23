# TOOL hfst-fst2strings.py: "Sample an archive"
#     (Produces a convenient sample of path labels in the transducers.
# These paths can be just some paths, best paths by weight, or random paths.
# This tool may not work correctly with optimized-lookup formats, according to its --help.)
# INPUT ducer.hfst: "Transducers" TYPE GENERIC
#     (An HFST transducer archive)
# OUTPUT sample.txt
# OUTPUT OPTIONAL version.log
# OUTPUT OPTIONAL stdout.log
# OUTPUT OPTIONAL stderr.log
# PARAMETER PathType
#     TYPE [path: "any path",
#           best: "best path",
#           random: "random path"]
#     DEFAULT random
#     (How to choose the paths through the transducer)
# PARAMETER SampleSize
#     TYPE [size_1000: "1000",
#           size_500: "500",
#           size_200: "200",
#           size_100: "100",
#           size_50: "50",
#           size_20: "20",
#           size_10: "10"]
#     DEFAULT size_50
#     (Maximum size of the sample)
# PARAMETER MaxCycles
#     TYPE [in_50: "50",
#           in_20: "20",
#           in_10: "10",
#           in_5: "5",
#           in_2: "2"]
#     DEFAULT in_10
#     (Maximum times to follow cycles)
# PARAMETER MaxInLength
#     TYPE [in_200: "200",
#           in_100: "100",
#           in_50: "50",
#           in_20: "20",
#           in_10: "10"]
#     DEFAULT in_200
#     (Maximum input length)
# PARAMETER MaxOutLength
#     TYPE [out_200: "200",
#           out_100: "100",
#           out_50: "50",
#           out_20: "20",
#           out_10: "10"]
#     DEFAULT out_200
#     (Maximum output length)
# PARAMETER Epsilon
#     TYPE [nothing: "as nothing",
#           underscore: "as _"]
#     DEFAULT nothing
#     (Whether to make empty labels of arcs visible)
# PARAMETER Version TYPE [v_3_14_0: "3.14.0"] DEFAULT v_3_14_0 (HFST version)
# PARAMETER VersionLog TYPE [omit: "omit version.log", produce: "produce version.log"] DEFAULT omit (Whether to produce --version log)

import sys
sys.path.append(os.path.join(chipster_module_path, "python"))
from lib_names2 import base, name
import lib_hfst as hfst

import os, shutil
from subprocess import Popen

name('sample.txt', base('ducer.hfst', '*.hfst'),
     ins = 'sample',
     ext = 'txt')

hfst.setenv(Version)

sampletype = dict(path = '--max-strings',
                  best = '--nbest',
                  random = '--random')[PathType]

_, samplesize = SampleSize.split('_')

_, maxcycles = MaxCycles.split('_')
_, inlength = MaxInLength.split('_')
_, outlength = MaxOutLength.split('_')

epsilon = dict(nothing = '',
               underscore = '_')[Epsilon]

with Popen(['hfst-fst2strings', '-o', 'sample.txt',
            sampletype, samplesize,
            '--cycles', maxcycles,
            '--max-in-length', inlength,
            '--max-out-length', outlength,
            '--epsilon-format', epsilon,
            'ducer.hfst'],
           stdout = open('stdout.log', mode = 'wb'),
           stderr = open('stderr.log', mode = 'wb')) as it:
    pass

hfst.finish(require = 'sample.txt',
            version = 'hfst-fst2strings' if VersionLog == 'produce' else None)
