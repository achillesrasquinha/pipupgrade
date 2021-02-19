# imports - standard imports
import os, os.path as osp

# imports - module imports
from pipupgrade.config import PATH, Settings
from pipupgrade.util.imports import import_handler
from pipupgrade import parallel, log

settings = Settings()
logger   = log.get_logger()

JOBS = [
    "build_proxy_list",
    "build_dependency_tree"
]

def run_all():
    logger.info("Running all jobs...")
    
    fns     = [import_handler("pipupgrade.jobs.%s.run" % job) for job in JOBS]

    njobs   = settings.get("jobs")

    for fn in fns:
        fn()