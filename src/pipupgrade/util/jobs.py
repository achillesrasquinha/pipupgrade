# imports - standard imports
import os, os.path as osp
from   functools import partial
import sys

# imports - module imports
from pipupgrade.config          import PATH, Settings
from pipupgrade.util.imports    import import_handler
from pipupgrade.util.system     import popen
from pipupgrade.util._dict      import merge_dict
from pipupgrade.util.environ    import getenvvar, getenv
from pipupgrade import parallel, log

settings = Settings()
logger   = log.get_logger()

JOBS = [
    { "name": "build_proxy_list" },
    {
        "name": "build_dependency_tree",
        "variables": {
            getenvvar("JOBS_GEVENT_PATCH"): True
        },
        # "beta": True
    }
]

def run_job(name, variables = None):
    job = [job for job in JOBS if job["name"] == name]
    if not job:
        raise ValueError("No job %s found." % name)
    else:
        job = job[0]

    variables = merge_dict(job.get("variables", {}), variables or {})

    popen("%s -c 'from pipupgrade.util.imports import import_handler; import_handler(\"%s\")()'" %
        (sys.executable, "pipupgrade.jobs.%s.run" % name), env = variables)

def run_all():
    logger.info("Running all jobs...")
    for job in JOBS:
        if not job.get("beta") or getenv("JOBS_BETA"):
            run_job(job["name"], variables = job.get("variables"))