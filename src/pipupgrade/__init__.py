try:
    import os

    if os.environ.get("PIPUPGRADE_JOBS_GEVENT_PATCH"):
        from gevent import monkey
        monkey.patch_all(threaded = False, select = False)
except ImportError:
    pass

# imports - module imports
from pipupgrade.__attr__    import (
    __name__,
    __version__,
    __author__
)
from pipupgrade.__main__    import main
from pipupgrade.config      import Settings
from pipupgrade             import _pip
from pipupgrade.util.jobs   import run_all as run_all_jobs, run_job

settings = Settings()

from pipupgrade.tree import Node