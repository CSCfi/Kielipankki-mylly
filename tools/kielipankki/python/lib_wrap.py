import os
import re
import shutil
import sys
import tempfile

from subprocess import Popen, PIPE, TimeoutExpired
from zipfile import ZipFile, BadZipFile

# TODO: These functions need to receive the file name ./data.wrap from
# the tool. Like the new restore_inputs(wrapname, tag) already does.

# To test outside Mylly: In Taito, where the underlying tools live,
# make test scripts that are like td-wrap.py and td-job.py but point
# their sys.path to the local clone of the repository; run your
# test-wrap.py in a directory that contains a ./text.txt; then run
# your test-job.py in a directory that contains the resulting
# ./data.wrap (the same directory will do just fine); unzip -l
# data.wrap to see where in your $WRKDIR the batch job is working.
#
# Adapt when the scripts acquire parameters and such.
#
# The "wrap" and "job" tools need to be paired because their chipster
# headers must specify input and output file names. Otherwise, "job"
# in particular is quite generic.

def setup_wrap(tag, *datadata):
    '''
    Wraps ./text.txt in ./data.wrap as ./data/text.txt

    Creates $WRKDIR/wrap<tmp>

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
        wrap.writestr("ticket/{}".format(name), "{}\n".format(tag))
        for data in datadata:
            # *should* check: text.txt or ./text.txt, like, in cwd;
            # but these names *do* come from a trusted Mylly tool.
            arcname = os.path.join("data", os.path.basename(data))
            wrap.write(data, arcname = arcname)
        # that does not seem to compress data - should one compress?

# There are so many ways to fail
class BadWrapFile(Exception): pass
class DifferentWrapFile(Exception): pass
class NoWorkDirectory(Exception): pass

def setup_job(tag, template):
    '''Make <path>/wrap.job for ./data.wrap, to be submitted to the
    batch system. The job template lacks only <path>, and <path> is
    already made in a standard location, its basename recorderd as
    ticket/<path> in ./data.wrap.

    Also store ./chipster-inputs.tsv to <path>. This way the display
    names never come directly from the user but are those that were
    already in use in the chipster interface.'''

    # should really check that data.wrap is there and is a zip file
    # and contains the ticket and ... well, actually
    # get_work_directory does check, and actually it was just made
    # when this function is called as intended.

    with ZipFile("data.wrap", "r") as wrap:
        path = get_work_directory(wrap, tag)

    with open(os.path.join(path, "wrap.job"), "w") as job:
        print(template.format(path = path), file = job)

    shutil.copy("./chipster-inputs.tsv", path)

def restore_inputs(wrapname, tag):
    '''To be called by the tools that run wrapped jobs, right in the
    start where they specify the display names of their outputs, this
    overrides their ./chipster-inputs.tsv with the one that specifies
    the wrapped files names.'''
    with ZipFile(wrapname, "r") as wrap:
        work = get_work_directory(wrap, tag)

    # should be there from the time the wrap was made, given that the
    # path could be resolved; always overrides the file in "."
    shutil.copy(os.path.join(work, "chipster-inputs.tsv"), ".")

# TODO: what is the following comment doing here?

'''
    First time td-job (another "tool") on ./data.wrap
    - checks ./data.wrap claims to be a "Turku Dependency Wrap"
    - creates $WRKDIR/<tmpdir>/state (expect this to be somewhat atomic)
    - extracts data/text.txt to $WRKDIR/<tmpdir>
    - sends $WRKDIR/<tmpdir>/wrap.job to a batch queue
    - touches $WRKDIR/<tmpdir>/state/started (that'll date it)
    - produces ./status.log from the queue

    Subsequent times td-job on ./data.wrap
    - produces ./status.log from the queue (wait, which queue? which job?)

    When td-job on ./data.wrap finds the job finished and result there, it
    - moves $WRKDIR/<tmpdir>/result.wev to ./analyses.txt (the result file)

    Questions:
    - does td-job hide log files from user or produce them? maybe on request?
    - etc
'''

def process_wrap(tag, *results):
    '''
    Process ./data.wrap as follows:

    Extract <name> from ticket/<name> in ./data.wrap, check that the
    member has tag (e.g. "Turku Dependency Wrap") on its first line.

    Try to create $WRKDIR/<name>/state/.
    
    - success -> extract data/* from ./data.wrap to
    $WRKDIR/<name>/data/ and submit $WRKDIR/<name>/wrap.job

    - failure because directory exists -> check job status

    - failure for some other reason -> error

    When checking job status, always report status.

    - if still in batch system -> ok

    - otherwise if finished -> produce results (error if not there)

    - otherwise -> error (and partial results if there)

    When job has left the system, also clean up the work directory.
    '''

    try:
        with ZipFile("data.wrap", "r") as wrap:

            work = get_work_directory(wrap, tag)

            # The next step should be atomic! Either actually make the
            # state/ directory now and proceed to submit the job, or
            # else raise the exception and proceed to check the state
            # of the previously submitted job.
            os.mkdir(os.path.join(work, "state"))

            # The state/ directory was made right now. Extract the
            # wrapped data and submit the job.
            datadata =  [ member for member in wrap.namelist()
                          if os.path.dirname(member) == "data" ]
            wrap.extractall(path = work, members = datadata)
            submit_job(work, results)

    except FileExistsError:
        # The existence of <work>/state/ indicates that the job has
        # already been submitted; produce ./status.log; if the job has
        # finished, produce ./analyses.txt (the actual result).
        check_job(work, results)

    except (BadZipFile, BadWrapFile):
        print("Input file is not a wrap file",
              file = sys.stderr)
        exit(29)

    except DifferentWrapFile:
        with open("status.log", "a") as log:
            print("Input wrap file cannot be processed with this tool",
                  file = log)

    except NoWorkDirectory:
        with open("status.log", "a") as log:
            print("Job directory for this wrap file is not found",
                  "",
                  "This is normal after a final status is reported,",
                  "at which time any results should have appeared.",
                  "",
                  "If an unfinished wrap is old, rewrap the data.",
                  sep = '\n',
                  file = log)

    # any other exceptions are unexpected and may fly


def get_work_directory(wrap, tag):
    name = get_ticket_name(wrap, tag)
    work = os.path.join(os.environ.get('WRKDIR'), name)

    if os.path.isdir(work):
        return work
    else:
        raise NoWorkDirectory()

def get_ticket_name(wrap, tag):
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

    with wrap.open(os.path.join("ticket", name)) as ticket:
        if tag.encode('UTF-8') in next(ticket, b''):
            return name
        else:
            raise DifferentWrapFile()

def submit_job(work, results):
    '''
    <work>/state/ is empty
    <work>/data/<whatever> is there (just extracted from data.wrap)
    <work>/wrap.job should be there (ever since data.wrap was made)

    submit wrap.job to the batch system, recording job number in state/started

    produce ./status.log (dated, with advice)

    '''

    with Popen(["sbatch", os.path.join(work, "wrap.job")],
               stdout = open(os.path.join(work, "state", "started"), mode = "wb"),
               stderr = open(os.path.join(work, "state", "sbatch.err"), mode ="wb")):
        pass

    check_job(work, results)

def check_job(work, results):
    '''

    <work>/state/started provides job number; apparently squeue
    *sometimes* considers it an error to request information on a
    COMPLETED job, but otherwise yes.

    '''

    status, message = get_status(work, get_number(work))

    with open("status.log", "w") as log:
        print(message, file = log)

    if status == "FAIL":
        print("TODO: produce a log on FAIL: job did not complete")

    if status in ("DONE", "FAIL"):
        finish_job(work, results)

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

def get_number(work):
    "What if this fails? "
    with open(os.path.join(work, "state", "started")) as started:
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

# should pay attention to error logs that the user wants to see, if
# any, so they are separate and can be consolidated to one error.log
