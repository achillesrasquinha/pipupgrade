# imports - standard imports
from   contextlib      import contextmanager
import multiprocessing as mp
from   multiprocessing.pool import Pool

from pipupgrade._compat import PYTHON_VERSION

USE_PROCESS_POOL_EXECUTOR = not (PYTHON_VERSION.major == 2 or (PYTHON_VERSION.major == 3 and PYTHON_VERSION.minor <= 7))

if USE_PROCESS_POOL_EXECUTOR:
    from concurrent.futures import ProcessPoolExecutor

    class NoDaemonPool(ProcessPoolExecutor):
        def imap_unordered(self, *args, **kwargs):
            return self.map(*args, **kwargs)
else:
    class NonDaemonProcess(mp.Process):
        @property
        def daemon(self):
            return False

        @daemon.setter
        def daemon(self, val):
            pass

    # https://github.com/nipy/nipype/pull/2754
    class NoDaemonPool(Pool):
        def __init__(self, *args, **kwargs):
            self.super = super(NoDaemonPool, self)
            self.super.__init__(*args, **kwargs)

        def Process(self, *args, **kwargs):
            process = self.super.Process(*args, **kwargs)
            process.__class__ = NonDaemonProcess
            return process

@contextmanager
def pool(class_ = Pool, *args, **kwargs):
    pool = class_(*args, **kwargs)
    yield pool

    if getattr(pool, "terminate", None):
        pool.terminate()

@contextmanager
def no_daemon_pool(*args, **kwargs):
    if USE_PROCESS_POOL_EXECUTOR:
        if "processes" in kwargs:
            kwargs["max_workers"] = kwargs.pop("processes")

    with pool(class_ = NoDaemonPool, *args, **kwargs) as p:
        yield p

        p.close(); p.join()