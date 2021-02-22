# imports - standard imports
import os, os.path as osp
import re
import asyncio
import csv

from proxybroker import Broker

from pipupgrade.exception       import PopenError
from pipupgrade.util.environ    import getenv
from pipupgrade.util.array      import chunkify
from pipupgrade.util.system     import make_temp_dir, popen, read, write
from pipupgrade.util.proxy      import (fetch as fetch_proxies, save as save_proxies_to_db,
    PROXY_COLUMNS)
from pipupgrade.util.request    import proxy_request
from pipupgrade.util.string     import safe_decode, strip
from pipupgrade.util.datetime   import get_timestamp_str
from pipupgrade.config          import PATH
from pipupgrade._compat import iterkeys, itervalues, iteritems
from pipupgrade import db
from pipupgrade import log

logger      = log.get_logger(level = log.DEBUG)
connection  = db.get_connection()

PROXY_LEVEL_CODES = {
    "High": "H",
    "Transparent": "T",
    "Anonymous": "A"
}

async def save_proxies(proxies):
    while True:
        proxy = await proxies.get()

        if proxy is None:
            break

        values = [ ]

        for type_, level in iteritems(proxy.types):
            secure  = int(type_ == "HTTPS")
            level   = PROXY_LEVEL_CODES[ level ] if level else None
            value   = (proxy.host, proxy.port, secure, level,
                proxy.geo.code, int(proxy.is_working), proxy.error_rate,
                proxy.avg_resp_time)

            values.append(value)

        save_proxies_to_db(values)

def run(*args, **kwargs):
    logger.info("Fetching Proxies...")

    fetch_proxies()

    proxies = asyncio.Queue()
    broker  = Broker(proxies)
    tasks   = asyncio.gather(
        broker.find(types = ["HTTP", "HTTPS"], limit = 100),
        save_proxies(proxies)
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

    logger.info("Commiting Latest Proxy List...")

    with make_temp_dir() as dir_path:
        repo = osp.join(dir_path, "proxy-list")

        github_username    = getenv("JOBS_GITHUB_USERNAME",    raise_err = True)
        github_oauth_token = getenv("JOBS_GITHUB_OAUTH_TOKEN", raise_err = True)

        popen("git clone https://%s:%s@github.com/achillesrasquinha/proxy-list.git %s" % 
            (github_username, github_oauth_token, repo), cwd = dir_path)

        popen("git config user.email 'bot.pipupgrade@gmail.com'", cwd = repo)
        popen("git config user.name  'pipupgrade bot'", cwd = repo)

        proxies_path = osp.join(repo, "proxies.csv")

        with open(proxies_path, "w") as f:
            f.write(PROXY_COLUMNS)
            f.write("\n")

            for row in connection.query("SELECT * FROM `tabProxies`"):
                values = itervalues(row)
                data   = ",".join(map(str, values))

                f.write(data)
                f.write("\n")

        write(proxies_path, strip(read(proxies_path)))

        popen("git add %s" % proxies_path, cwd = repo)
        commit_message = "Update Proxy List: %s" % get_timestamp_str()
        popen("git commit --allow-empty -m '%s'" % commit_message, cwd = repo)

        popen("git push origin master", cwd = repo)

        logger.info("Proxy List upto date.")