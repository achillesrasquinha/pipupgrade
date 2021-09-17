<<<<<<< HEAD
from __future__ import absolute_import

=======

from __future__ import absolute_import


>>>>>>> template/master
try:
    import os

    if os.environ.get("PIPUPGRADE_GEVENT_PATCH"):
        from gevent import monkey
        monkey.patch_all(threaded = False, select = False)
except ImportError:
    pass

# imports - module imports
<<<<<<< HEAD
from pipupgrade.__attr__  import (
    __name__,
    __version__,
    __author__
)
from pipupgrade.__main__  import main
from bpyutils.config      import Settings, get_config_path

settings = Settings(location = get_config_path(__name__))
=======
from pipupgrade.__attr__ import (
    __name__,
    __version__,


    __description__,

    __author__
)
from pipupgrade.__main__    import main
from bpyutils.config      import Settings
from bpyutils.util.jobs   import run_all as run_all_jobs, run_job

settings = Settings()


def get_version_str():
    version = "%s%s" % (__version__, " (%s)" % __build__ if __build__ else "")
    return version
>>>>>>> template/master
