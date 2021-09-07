try:
    import os

    if os.environ.get("PIPUPGRADE_GEVENT_PATCH"):
        from gevent import monkey
        monkey.patch_all(threaded = False, select = False)
except ImportError:
    pass

# imports - module imports
from pipupgrade.__attr__  import (
    __name__,
    __version__,
    __author__
)
from pipupgrade.__main__  import main
from bpyutils.config      import Settings, get_config_path

settings = Settings(location = get_config_path(__name__))