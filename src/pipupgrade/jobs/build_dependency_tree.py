import os.path as osp

# imports - standard imports
import requests as req
from xmlrpc.client import ServerProxy as XMLRPCConnector
from bs4 import BeautifulSoup

import grequests
from tqdm import tqdm
from fake_useragent import UserAgent

from pipupgrade.config       import PATH
from pipupgrade._compat      import iterkeys
from pipupgrade.util.request import proxy_request, get_random_requests_proxies as get_rand_proxy
from pipupgrade.util.system  import read, write, make_temp_dir
from pipupgrade.util.string  import safe_decode
from pipupgrade.util.array   import chunkify
from pipupgrade import log

BASE_INDEX_URL = "https://pypi.org/simple"

logger      = log.get_logger(level = log.DEBUG)
user_agent  = UserAgent()

def exception_handler(request, exception):
    logger.warning("Unable to load request: %s", exception)

def run(*args, **kwargs):
    with make_temp_dir() as dir_path:
        chunk_size  = kwargs.get("chunk_size", 1000)
        index_url   = kwargs.get("index_url", BASE_INDEX_URL)

        logger.info("Fetching Package List...")

        res = proxy_request("GET", index_url, stream = True)
        res.raise_for_status()

        html = ""
        for content in res.iter_content(chunk_size = 1024):
            html += safe_decode(content)

        soup = BeautifulSoup(html, 'html.parser')

        packages        = list(map(lambda x: x.text, soup.findAll('a')))
        logger.info("%s packages found." % len(packages))
        
        package_chunks  = list(chunkify(packages, chunk_size))

        connector       = XMLRPCConnector(index_url)

        for package_chunk in tqdm(package_chunks):
            requestsmap = (
                grequests.get("https://pypi.org/pypi/%s/json" % package,
                    proxies = get_rand_proxy(),
                    headers = { "User-Agent": user_agent.random }
                ) for package in package_chunk
            )

            responses   = grequests.map(requestsmap,
                exception_handler = exception_handler)

            for response in responses:
                if response.ok:
                    data     = response.json()
                    releases = list(iterkeys(data["releases"]))
                else:
                    logger.info("Unable to load URL: %s" % response.url)