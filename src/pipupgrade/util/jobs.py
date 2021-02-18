# imports - standard imports
import os, os.path as osp

# imports - module imports
from pipupgrade.config import PATH, Settings
from pipupgrade.util.imports import import_handler
from pipupgrade import parallel, log

settings = Settings()
logger   = log.get_logger()

def run_all():
    logger.info("Running all jobs...")

    jobs    = os.listdir(PATH["JOBS"])
    paths   = [osp.splitext(p)[0] for p in jobs if p not in ("__init__.py", "__pycache__")]
    
    logger.info("Jobs found: %s" % paths)
    
    fns     = [import_handler("pipupgrade.jobs.%s.run" % fn) for fn in paths]

    njobs   = settings.get("jobs")

    # with parallel.pool(processes = njobs) as pool:
    #     jobs = [pool.map(fn, [None]) for fn in fns]

    for fn in fns:
        fn()