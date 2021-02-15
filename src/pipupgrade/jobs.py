import re
import os.path as osp

import requests as req
from bs4 import BeautifulSoup

from pipupgrade.db              import get_connection
from pipupgrade.util.string     import safe_decode
from pipupgrade.util.system     import popen, make_temp_dir
from pipupgrade.util.request    import proxy_request
from pipupgrade.log             import get_logger
from pipupgrade._compat         import iterkeys, itervalues
from pipupgrade.db              import get_connection

BASE_INDEX_URL      = "https://pypi.org/simple"
REGEX_PROXY_STRING  = r"^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]) (?P<country_code>[A-Z][A-Z])-(?P<anonymity>N|A|H)?(?P<protocol>\s|-S)?(?P<one_way>\!)? (?P<google_passed>\+|-)"

logger  = get_logger()
db      = get_connection()

def build_dependency_tree(index_url = BASE_INDEX_URL):
    res = req.get(index_url, stream = True)

    if res.ok:
        html = ""
        for content in res.iter_content(chunk_size = 1024):
            html += safe_decode(content)

        soup = BeautifulSoup(html, 'html.parser')

        packages = list(map(lambda x: x.text, soup.findAll('a')))

        for package in packages:
            res  = req.get("https://pypi.org/simple/%s" % package)
            soup = BeautifulSoup(res.content, 'html.parser')

            if res.ok:
                versions = list(map(lambda x: x.text, soup.findAll('a')))
                break
            else:
                res.raise_for_status()
    else:
        res.raise_for_status()

def build_proxy_list():
    with make_temp_dir() as dir_path:
        repo = osp.join(dir_path, "repo")
        popen("git clone https://github.com/clarketm/proxy-list %s" % repo, cwd = dir_path)
        _, output, _ = popen("git log --reverse --pretty=format:'%h'", cwd = repo, output = True)
        hashes = output.split("\n")

        for hash_ in hashes:
            url = "https://raw.githubusercontent.com/clarketm/proxy-list/%s/proxy-list.txt" % hash_
            logger.info("Loading url %s..." % url)

            res = proxy_request("GET", url)
            # res = req.get(url)

            if res.ok:
                content = safe_decode(res.content)
                lines   = content.split("\n")

                for line in lines:
                    output = re.match(REGEX_PROXY_STRING, line)
                    if output:
                        output = output.groupdict()

                        # sanitize output
                        output["protocol"]      = "https" if output["protocol"] else "http"
                        output["one_way"]       = output["one_way"] == "!"
                        output["google_passed"] = output["google_passed"] == "+"

                        keys    = ", ".join(iterkeys(output))
                        values  = ", ".join(map(lambda x: "'%s'" % x, itervalues(output)))

                        logger.info("Saving proxy %s...", output)

                        db.query("""
                            INSERT INTO `tabProxies`
                                (%s)
                            VALUES
                                (%s)
                        """ % ( keys , values ))
            else:
                logger.warn("Unable to load URL %s" % url)