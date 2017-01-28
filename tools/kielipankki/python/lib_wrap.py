import os
import shutil
import sys
import tempfile

from subprocess import Popen, PIPE, TimeoutExpired
from zipfile import ZipFile, BadZipFile

# To test: run td-wrap.py in a directory that contains a text.txt but
# no data.wrap; then run td-job.py (this script) in a directory that
# contains the resulting data.wrap; unzip -l data.wrap to see where in
# $WRKDIR the batch job is working.
#
# Make test scripts, like so:
#
#    # testwrap.py
#    sys.path.append("/dir/where/lib/is")
#    import lib_wrap as lib
#    lib.setup_wrap(b"Turku Dependency Wrap", "./text.txt")
#    lib.setup_job(b"Turku Dependency Wrap", "... {path} ...")
#
#    # testjob.py
#    sys.path.append("/dir/where/lib/is")
#    import lib_wrap is lib
#    lib.process_wrap(b"Turku Dependency Wrap")
#
# "wrap" and "job" need to be paired because they must specify input
# and output file names in their chipster header - other than that,
# "job" is quite generic.

def setup_wrap(tag, *datadata):
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
        wrap.writestr("ticket/{}".format(name), "{}\n".format(tag))
        for data in datadata:
            # *should* check: text.txt or ./text.txt, like, in cwd
            arcname = os.path.join("data", os.path.basename(data))
            wrap.write(data, arcname = arcname)
        # that does not seem to compress data - should one compress?

# There are so many ways to fail
class WrapError(Exception): pass
class WorkError(Exception): pass

def setup_job(tag, template):
    '''Make <path>/wrap.job for ./data.wrap, to be submitted to the
    batch system. The job template lacks only <path>, and <path> is
    already made in a standard location, its basename recorderd as
    ticket/<path> in ./data.wrap.'''

    # should really check that data.wrap is there and is a zip file
    # and contains the ticket and ... well, actually
    # get_work_directory does check, and actually it was just made
    # when this function is called as intended.

    with ZipFile("data.wrap", "r") as wrap:
        path = get_work_directory(wrap, tag)

    with open(os.path.join(path, "wrap.job"), "w") as job:
        print(template.format(path = path), file = job)

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

    except (BadZipFile, WrapError):
        print("Input is not a valid wrap of the present kind",
              file = sys.stderr)
        exit(29)

    except WorkError:
        with open("status.log", "a") as log:
            print("Job is gone.",
                  "",
                  "An internal directory for this wrap was not found.",
                  "This is normal after a final status is reported,",
                  "at which time any results should also have appeared.",
                  "",
                  "If an unfinished wrap is old, rewrap the data.",
                  sep = '\n',
                  file = sys.stderr)

    # any other exceptions are unexpected and may fly


def get_work_directory(wrap, tag):
    name = get_ticket_name(wrap, tag)
    work = os.path.join(os.environ.get('WRKDIR'), name)

    if os.path.isdir(work):
        return work
    else:
        raise WorkError()

def get_ticket_name(wrap, tag):
    """Get ticket name "wrap*" from the wrap (a ZipFile). There should
    be exactly one member ticket/wrap*, and that member should also
    contain the tag that indicates the use of this script. Raise
    WrapError() if this is not the case."""

    ticketnames = [ member
                    for member in wrap.namelist()
                    if os.path.dirname(member) == "ticket"
                    if os.path.basename(member).startswith("wrap") ]

    if len(ticketnames) == 1:
        [ticketname] = ticketnames
    else:
        raise WrapError()

    with wrap.open(ticketname) as ticket:
        if tag.encode('UTF-8') in next(ticket, b''):
            return os.path.basename(ticketname)
        else:
            raise WrapError()

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
    DONE if job is (not in queue and) is finished
    FAIL if job is not in queue but is not finished either

    What if <work> is not ok? Can one get here then?
    '''

    with Popen(["squeue", "--jobs", number],
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

    if number in out:
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
