import os.path as osp
import shutil
import json

# imports - standard imports
import requests as req
import grequests
from bs4 import BeautifulSoup
from addict import Dict

from tqdm import tqdm

from pipupgrade.config          import PATH
from pipupgrade._compat         import iterkeys
from pipupgrade.util.request    import proxy_request, proxy_grequest, get_random_requests_proxies as get_rand_proxy
from pipupgrade.util.system     import read, write, make_temp_dir, popen
from pipupgrade.util.string     import safe_decode
from pipupgrade.util.array      import chunkify
from pipupgrade.util.datetime   import get_timestamp_str
from pipupgrade.util.environ    import getenv
from pipupgrade.util._dict      import autodict
from pipupgrade import log, db

BASE_INDEX_URL  = "https://pypi.org/simple"
logger          = log.get_logger(level = log.DEBUG)
connection      = db.get_connection()

def exception_handler(request, exception):
    logger.warning("Unable to load request: %s", exception)

def run(*args, **kwargs):
    dir_path = PATH["CACHE"]

    # seed database...
    repo = osp.join(dir_path, "pipupgrade-assets")

    if not osp.exists(repo):
        github_username    = getenv("JOBS_GITHUB_USERNAME",    raise_err = True)
        github_oauth_token = getenv("JOBS_GITHUB_OAUTH_TOKEN", raise_err = True)

        popen("git clone https://%s:%s@github.com/achillesrasquinha/pipupgrade-assets %s" %
            (github_username, github_oauth_token, repo), cwd = dir_path)

        popen("git config user.email 'bot.pipupgrade@gmail.com'", cwd = repo)
        popen("git config user.name  'pipupgrade bot'", cwd = repo)
    else:
        try:
            popen("git pull origin master", cwd = repo)
        except PopenError:
            logger.warn("Unable to pull latest branch")

    path_deptree = osp.join(repo, "dependencies.json")
    deptree      = Dict()

    if osp.exists(path_deptree):
        with open(path_deptree) as f:
            deptree = Dict(json.load(f))

    with make_temp_dir() as dir_path:
        chunk_size  = kwargs.get("chunk_size", 1000)
        index_url   = kwargs.get("index_url", BASE_INDEX_URL)

        logger.info("Fetching Package List...")

        res  = proxy_request("GET", index_url, stream = True)
        res.raise_for_status()

        html = ""
        for content in res.iter_content(chunk_size = 1024):
            html += safe_decode(content)

        soup = BeautifulSoup(html, 'html.parser')

        packages = list(map(lambda x: x.text, soup.findAll('a')))

        logger.info("%s packages found." % len(packages))

        package_chunks  = list(chunkify(packages, chunk_size))

        for package_chunk in tqdm(package_chunks):
            requestsmap = (
                proxy_grequest("GET", "https://pypi.org/pypi/%s/json" % package)
                    for package in package_chunk
            )

            responses   = grequests.map(requestsmap,
                exception_handler = exception_handler)

            for response in responses:
                if response.ok:
                    data     = response.json()
                    package  = data["info"]["name"]
                    releases = list(iterkeys(data["releases"]))

                    release_chunks = chunkify(releases, 100)

                    for release_chunk in release_chunks:
                        requestsmap = (
                            proxy_grequest("GET", "https://pypi.org/pypi/%s/%s/json" % (package, release))
                                for release in release_chunk
                        )

                        responses = grequests.map(requestsmap,
                            exception_handler = exception_handler)

                        for response in responses:
                            if response.ok:
                                data     = response.json()
                                version  = data["info"]["version"]
                                requires = data["info"]["requires_dist"]

                                deptree[package][version] = requires

                                # query    = """
                                #     INSERT OR IGNORE INTO `tabPackageDependency`
                                #         (name, version, requires)
                                #     VALUES
                                #         (?, ?, ?)
                                # """
                                # values   = (
                                #     package,
                                #     version,
                                #     ",".join(requires) if requires else "NULL"
                                # )

                                # connection.query(query, values)
                            else:
                                logger.info("Unable to load URL: %s" % response.url)
                else:
                    logger.info("Unable to load URL: %s" % response.url)

            with open(path_deptree, mode = "w") as f:
                json.dump(deptree, f)

            popen("git add %s" % path_deptree, cwd = repo)
            popen("git commit --allow-empty -m 'Update database: %s'" % get_timestamp_str(),
                cwd = repo)
            popen("git push origin master", cwd = repo)