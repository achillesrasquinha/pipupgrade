# imports - standard imports
import os.path as osp
import asyncio

import requests as req
import grequests as greq
from proxybroker import Broker
from tqdm import tqdm

from bpyutils.util.environ    import getenv
from bpyutils.util.system     import make_temp_dir, popen, read, write
from bpyutils.util.proxy      import (fetch as fetch_proxies, save as save_proxies_to_db,
    PROXY_COLUMNS)
from bpyutils.util.array      import chunkify
from bpyutils.util.string     import strip
from bpyutils.util.datetime   import get_timestamp_str
from bpyutils._compat         import itervalues, iteritems
from bpyutils.config          import get_config_path

from pipupgrade.__attr__ import __name__ as NAME
from bpyutils import log, db

logger      = log.get_logger(name = NAME, level = log.DEBUG)
connection  = db.get_connection(location = get_config_path(NAME)))

import aiohttp

from proxybroker.resolver import Resolver
from proxybroker.utils import log

PROXY_LEVEL_CODES = {
    "High": "H",
    "Transparent": "T",
    "Anonymous": "A"
}

# https://github.com/constverum/ProxyBroker/issues/141#issuecomment-628080856
class CustomResolver(Resolver):
    _c_ip_hosts = [ ]

    def _get_random_ip_host(self):
        host = random.choice(self._c_ip_hosts)
        self._c_ip_hosts.remove(host)
        return host

    async def get_real_ext_ip(self):
        self._c_ip_hosts = self._ip_hosts.copy()
        while self._c_ip_hosts:
            try:
                timeout = aiohttp.ClientTimeout(total = self._timeout)
                async with aiohttp.ClientSession(
                    timeout = timeout, loop = self._loop
                ) as session, session.get( self._get_random_ip_host() ) as response:
                    print("foobar")
                    ip = await response.text()
            except asyncio.TimeoutError:
                pass
            else:
                ip = strip(ip)
                if self.host_is_ip(ip):
                    logger.debug("Real external IP:", ip)
                    break
        else:
            raise RuntimeError("Could not get the external IP")

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

def exception_handler(request, err):
    if not isinstance(err, (
        req.exceptions.Timeout,
        req.exceptions.ConnectionError,
        req.exceptions.TooManyRedirects
    )):
        # raise err
        pass

def check_proxies(timeout_threshold = 5):
    nchunks = 100
    rows    = connection.query("SELECT * FROM `tabProxies`")
    
    chunks  = list(chunkify(rows, nchunks))
    ids     = [ ]

    for chunk in tqdm(chunks):
        requests_map = [ ]
        rows         = list(chunk)
        
        for row in rows:
            type_ = "http" if not row["secure"] else "https"
            addr  = "%s://%s" % (type_, to_addr(row))
            # addr  = to_addr(row)

            proxies  = { type_: addr }
            url      = "%s://www.google.com" % type_

            request  = greq.get(url, proxies = proxies, timeout = timeout_threshold)
            requests_map.append(request)
        
        responses = greq.map(requests_map, exception_handler = exception_handler)
        for i, response in enumerate(responses):
            if not (response and response.ok):
                ids.append(rows[i]["id"])

        if ids:
            logger.info("Deleting %s proxies." % len(ids))
            connection.query("DELETE FROM `tabProxies` WHERE rowid IN (%s)" % ",".join(map(str,ids)))
            ids = [ ]

def _write_proxies(repo, fname = "proxies"):
    proxies_path = osp.join(repo, "%s.csv" % fname)

    with open(proxies_path, "w") as f:
        f.write(PROXY_COLUMNS)
        f.write("\n")

        for row in connection.query("SELECT %s FROM `tabProxies`" % PROXY_COLUMNS):
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

def run(*args, **kwargs):
    logger.info("Fetching Proxies...")

    fetch_proxies(fname = "proxies-all")

    loop    = asyncio.get_event_loop()

    # proxies = asyncio.Queue()
    # broker  = Broker(proxies)

    # # broker._resolver = CustomResolver(loop = loop)
    
    # tasks   = asyncio.gather(
    #     broker.find(types = ["HTTP", "HTTPS"], limit = 100),
    #     save_proxies(proxies)
    # )

    # loop.run_until_complete(tasks)

    logger.info("Commiting Latest Proxy List...")

    with make_temp_dir() as dir_path:
        repo = osp.join(dir_path, "proxy-list")

        github_username    = getenv("JOBS_GITHUB_USERNAME",    raise_err = True)
        github_oauth_token = getenv("JOBS_GITHUB_OAUTH_TOKEN", raise_err = True)

        popen("git clone https://%s:%s@github.com/achillesrasquinha/proxy-list.git %s" % 
            (github_username, github_oauth_token, repo), cwd = dir_path)

        popen("git config user.email 'bot.pipupgrade@gmail.com'", cwd = repo)
        popen("git config user.name  'pipupgrade bot'", cwd = repo)

        _write_proxies(repo, "proxies-all")

        logger.info("Checking Proxies...")
        check_proxies()
        
        _write_proxies(repo)