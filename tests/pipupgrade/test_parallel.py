# imports - module imports
from pipupgrade import parallel

def test_pool():
    def _assert(pool):
        results = pool.map(sum, [(1, 2), (3, 4)])

        assert results[0] == 3
        assert results[1] == 7

    with parallel.pool() as pool:
        _assert(pool)

    with parallel.pool(class_ = parallel.NoDaemonPool) as pool:
        _assert(pool)

    with parallel.no_daemon_pool() as pool:
        _assert(pool)