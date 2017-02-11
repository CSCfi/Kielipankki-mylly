import os
import re
import shutil
import sys
import time
import tempfile

from subprocess import Popen, PIPE, TimeoutExpired
from zipfile import ZipFile, BadZipFile

# TO REPLACE lib_wraps.py - A BETTER DESIGN! Make this so that a job
# file contains *only* the ticket and the data is already in the work
# directory and the job already submitted to the batch system
# (setup_wrap -> submit). Instead of a "run" tool, there is a "wait"
# tool that waits for the *results* in one step.  And a *generic*
# status checkinf tool! Submit and wait come in pairs, but there is
# one check for all. Brillant! (Think workflow, think no *spurious*
# optionality, no spurious copy of the data in a session, yet the
# ability to poll the job is there. A wait should mostly sleep.)

# Use the wrapname in the tool header. ***sorry what***
#
# Adapt when the scripts acquire parameters and such.
#
# The "submit" and "wait" tools need to be paired because their
# Chipster headers must specify input and output file names.
# Otherwise, "wait" in particular is quite generic ***is it*** and a
# status checking tool is more generic still.

def submit(jobname, tag, template, *datadata):
    '''
    Creates $WRKDIR/wrap<tmp>, outside chipster control!
    Creates $WRKDIR/wrap<tmp>/wrap.job from template.
    Copies ./chipster-inputs.tsv to $WRKDIR/wrap<tmp>/.
    Creates $WRKDIR/wrap<tmp>/state/.
    Creates $WRKDIR/wrap<tmp>/data/.
    Copies all datadata there.

    Saves "sbatch" output in state/sbatch.out where the job number can
    then be extracted.

    The datadata are meant to be just basenames without any path.

    ./data.job (jobname) is a zip archive file containing
    ticket/wrap<tmp> with the tag on its first line; this is all that
    a user could meaningfully try to forge and they are not supposed
    to know what other <tmp> are extant; even this could be encrypted
    but is that not overkill? This script would hardwire a password,
    and it would be a hassle to change it, for not much gain at all.
    '''

    work = tempfile.mkdtemp(prefix = 'wrap', dir = os.environ['WRKDIR'])

    with open(os.path.join(work, "wrap.job"), "w") as job:
        print(template.format(path = work), file = job)

    shutil.copy("./chipster-inputs.tsv", work)

    os.mkdir(os.path.join(work, "data"))
    for data in datadata:
        shutil.copy(data, os.path.join(work, "data"))

    os.mkdir(os.path.join(work, "state"))
    with Popen(["sbatch", os.path.join(work, "wrap.job")],
               stdout = open(os.path.join(work, "state", "sbatch.out"), mode = "wb"),
               stderr = open(os.path.join(work, "state", "sbatch.err"), mode = "wb")):
        pass

    with ZipFile(jobname, "w") as job:
        # one is on Python 3.4
        # since Python 3.5 one could create new archive with mode "x"
        # since Python 3.6 one could open an archive member with mode "w"
        name = os.path.basename(work)
        job.writestr("ticket/{}".format(name), "{}\n".format(tag))

    # might also produce an initial status.log here, sibling to ./data.job


def check(jobname):
    '''
    Produce a report on the state of the job, if the job is still
    there in the batch system.

    <work>/state/sbatch.out provides job number; apparently squeue
    *sometimes* considers it an error to request information on a
    COMPLETED job, but otherwise yes.

    '''

    work, number = get_job(jobname)
    status, message = get_status(work, get_number(work))

    with open("state.log", "w") as log:
        print(message, file = log)

# should pay attention to error logs that the user wants to see, if
# any, so they are separate and can be consolidated to one error.log

# There are so many ways to fail
class BadWrapFile(Exception): pass
class DifferentWrapFile(Exception): pass
class NoWorkDirectory(Exception): pass

def restore_inputs(jobname, tag):
    '''To be called by the tools that wait for submitted jobs, right
    in the start where they specify the display names of their own
    outputs, this overrides their ./chipster-inputs.tsv with the one
    that specifies the original display names.'''
    with ZipFile(jobname, "r") as wrap:
        work = get_work_directory(wrap, tag)

    # should be there from the time the job file was made, given that
    # the path could be resolved; always overrides the file in "."
    shutil.copy(os.path.join(work, "chipster-inputs.tsv"), ".")

def wait(jobname, tag, *results):
    '''
    Wait for the job to leave the batch system, produce any results in
    Chipster, clean up the work directory.
    '''

    work, number = get_job(jobname, tag)

    try:
        os.mkdir(os.path.join(work, "state", "waited"))
    except FileExistsError:
        print('This job is already waited',
              file = sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print('This job is not available any more',
              file = sys.stderr)
        sys.exit(1)

    while True:
        status, message = get_status(work, number)
        if status == "WAIT":
            time.sleep(5.0)
        elif status == "DONE":
            success(results, work)
            return
        elif status == "FAIL":
            failure(results, work)
            return
        else:
            raise ThisCannotHappen(status, message) # FIX THIS

# Re success, failure: need to consider partial results on failure and
# whether there needs to be any status.log on the results - the user
# experience, that is the question.

def success(results, work):
    finish_job(work, results)

def failure(results, work):
    finish_job(work, results)

def get_job(jobname, tag = None):
    '''Return work directory and job number, or exit with failure
    status. Check tag if provided.'''

    try:
        with ZipFile(jobname, "r") as wrap:
            work = get_work_directory(wrap, tag)
            return work, get_number(work)

    except (BadZipFile, BadWrapFile):
        print("This is not a job file.",
              file = sys.stderr)
        sys.exit(1)

    except DifferentWrapFile:
        print("This job file needs another tool.",
              file = sys.stderr)
        sys.exit(1)

    except NoWorkDirectory:
        print("The job directory was not found.",
              "The job may have finished already.",
              sep = '\n',
              file = sys.stderr)
        sys.exit(1)

def get_work_directory(wrap, tag = None):
    name = get_ticket_name(wrap, tag)
    work = os.path.join(os.environ.get('WRKDIR'), name)

    if os.path.isdir(work):
        return work
    else:
        raise NoWorkDirectory()

def get_ticket_name(wrap, tag = None):
    """Get ticket name "wrap*" from the wrap (a ZipFile). There should
    be exactly one member ticket/wrap*, and that member should also
    contain the tag that indicates the use of this script. Raise
    BadWrapFile() if this is not the case."""

    names = [ os.path.basename(member)
              for member in wrap.namelist()
              if os.path.dirname(member) == "ticket" ]

    if len(names) == 1:
        [name] = names
    else:
        raise BadWrapFile()

    # Supposing a malicious user has managed to graft a wrap-like zip
    # file with suprising characters in the ticket file name, do not
    # recognize the file as a wrap file in Mylly; str.almum is too
    # strict because tempfile.mkdtemp produces underscores; \w+ allows
    # underscores and re.ASCII restricts it to allow only ASCII.
    if not re.fullmatch('wrap\w+', name, re.ASCII):
        raise BadWrapFile()

    # It remains _possible_ to process an existing TMPDIR/wrap*
    # directory through a carefully grafted wrap-like file in Mylly.
    # The attacker needs to guess the random part of the name, and
    # still cannot _create_ a new directory or inject any data to the
    # existing (usually short-lived) directory except through the
    # intended processing mechanism, so the risk should be low.

    if tag is None:
        return name

    with wrap.open(os.path.join("ticket", name)) as ticket:
        if tag.encode('UTF-8') in next(ticket, b''):
            return name
        else:
            raise DifferentWrapFile()

def get_number(work):
    "What if this fails? "
    with open(os.path.join(work, "state", "sbatch.out")) as started:
        # "Submitted batch job 12151414\n" => "12151414"
        [number] = filter(str.isdigit, started.read().split())
        return number

def get_status(work, number):
    '''
    WAIT if job is still in queue (PENDING, RUNNING, COMPLETING, whatever)
    DONE if job (is not in queue and) is finished
    FAIL if job is not in queue but is not finished either

    What if <work> is not ok? Can one get here then?
    '''

    with Popen(["squeue", "--jobs", number,
                "--noheader",
                "--format",
                "\n".join(("Job %i %T in %P (reasons %r %R)",
                           "account %a, submitted %V",
                           "time limit %l, memory %m MB",
                           "nodes %D, processors/node %C",
                           "start %S",
                           "end   %E",
                           "left  %L"))],
               stdout = PIPE,
               stderr = PIPE) as poll:
        # encoding = "UTF-8" added in Python 3.6
        try:
            out, err = poll.communicate(timeout = 5) # seconds
            ret = 'Poll returned with code {}'.format(poll.returncode)
        except TimeOutExpired:
            poll.kill()
            out, err = poll.communicate()
            ret = 'Poll timed out'

    out = out.decode('UTF-8')
    err = err.decode('UTF-8')

    if out: # number in out: not sure what can be relied to indicate
        # that the job is still there - COMPLETED jobs seem to not be,
        # yet that is a valid state, but assume for now that really
        # finished jobs produce an empty report
        return "WAIT", '\n'.join(("Job is still in the batch system", "",
                                  "Poll stdout:", out,
                                  "Poll stderr:", err, ret))

    finished = os.path.exists(os.path.join(work, "state", "finished"))

    if finished:
        return "DONE", '\n'.join(("Job has run and has left the batch system", "",
                                  "Poll stdout:", out,
                                  "Poll stderr:", err, ret))

    return "FAIL", '\n'.join(("Job has failed to run and has left the batch system", "",
                              "Poll stdout:", out,
                              "Poll stderr:", err, ret))

def finish_job(work, results):
    """Move results, if any, over to ., and clean out the work
    directory."""

    for result in results:
        if ( os.path.dirname(result) not in ('', '.') or
             os.path.basename(result) in ('', '.', '..') ):
            with open("error.log", "a") as log:
                print("disallowed result filename:",
                      result,
                      file = log)
                continue

        it = os.path.join(work, os.path.basename(result))
        if os.path.exists(it):
            shutil.move(it, result)
        else:
            with open("error.log", "a") as log:
                # should be a numbered log! to consolidate at end!
                print("possible result file not in work directory:",
                      result,
                      file = log)

    if os.path.basename(work).startswith("wrap"):
        shutil.rmtree(work)
    else:
        # this cannot happen (or, is an error in this script)
        raise ResourceWarning("not removing {}".format(work))
