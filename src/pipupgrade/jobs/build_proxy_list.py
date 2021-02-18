# imports - standard imports
import os.path as osp
import re

import grequests
from tqdm import tqdm
from fake_useragent import UserAgent

from pipupgrade.util.environ    import getenv
from pipupgrade.util.array      import chunkify
from pipupgrade.util.system     import make_temp_dir, popen, read, write
from pipupgrade.util.request    import proxy_request
from pipupgrade.util.string     import safe_decode, strip
from pipupgrade.util.proxy      import to_str as proxy_to_str, to_dict as proxy_to_dict
from pipupgrade.util.request    import get_random_requests_proxies as get_rand_proxy
from pipupgrade.util.datetime   import get_timestamp_str
from pipupgrade.config          import PATH
from pipupgrade._compat import iterkeys, itervalues
from pipupgrade import db
from pipupgrade import log

logger      = log.get_logger(level = log.DEBUG)
connection  = db.get_connection()
user_agent  = UserAgent()

def request_exception_handler(request, exception):
    logger.error("Error while executing request %s: %s" % (request.url, exception))

def _save_proxies(proxies):
    keys    = ", ".join(iterkeys(proxies[0]))

    inserts = [ "INSERT OR IGNORE INTO `tabProxies` (%s) VALUES (%s);" % (
            keys, ", ".join(map(lambda x: "'%s'" % x, itervalues(p)))
        ) for p in proxies ]

    if inserts:
        connection.query("""
            BEGIN TRANSACTION;
            %s
            COMMIT;
        """ % "\n".join(inserts), script = True)

REGEX_IP_STATUS = r"^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}): (?P<status>success|failure)?"

def _build_status_map(statuses):
    status_map = { }

    for status in statuses:
        output = re.match(REGEX_IP_STATUS, status)
        
        if output:
            output = output.groupdict()
            status_map[ output["ip"] ] = int(output["status"] == "success")

    return status_map

def run(*args, **kwargs):
    dir_path = PATH["CACHE"]

    # seed database...
    repo = osp.join(dir_path, "proxy-list")

    if not osp.exists(repo):
        popen("git clone https://github.com/achillesrasquinha/proxy-list %s" % repo, cwd = dir_path)
    else:
        popen("git fetch --all", cwd = repo)

    proxy_list_path = osp.join(repo, "proxies.txt")

    # if osp.exists(proxy_list_path):
    #     logger.info("Reading fetched cached proxies...")

    #     lines   = read(proxy_list_path)
    #     proxies = list(filter(bool, lines.split("\n"))) # BUG?
    #     if proxies:
    #         logger.info("Saving fetched cached proxies...")
    #         _save_proxies(list(map(proxy_to_dict, proxies)))

    chunks  = kwargs.get("chunks", 350)

    repo    = osp.join(dir_path, "clarketm-proxy-list")

    if not osp.exists(repo):
        popen("git clone https://github.com/clarketm/proxy-list %s" % repo, cwd = dir_path)
    else:
        popen("git fetch --all", cwd = repo)

    _, output, _ = popen("git log --reverse --pretty=format:'%h'", cwd = repo, output = True)

    cache_path = osp.join(PATH["CACHE"], "proxy-list-hashes.txt")
    cached_hashes = read(cache_path) if osp.exists(cache_path) else ""

    hashes      = list(filter(lambda x: x not in cached_hashes, output.split("\n")))
    hash_chunks = list(chunkify(hashes, chunks))

    for hash_chunk in tqdm(hash_chunks):
        requestsmap_l, requestsmap_s = [], []
        for hash_ in hash_chunk:
            requestsmap_l.append(
                grequests.get("https://raw.githubusercontent.com/clarketm/proxy-list/%s/proxy-list.txt" % hash_,
                    # proxies = get_rand_proxy(),
                    headers = { "User-Agent": user_agent.random }
                )
            )
            requestsmap_s.append(
                grequests.get("https://raw.githubusercontent.com/clarketm/proxy-list/%s/proxy-list-status.txt" % hash_,
                    # proxies = get_rand_proxy(),
                    headers = { "User-Agent": user_agent.random }
                )
            )

        responses_l = grequests.map(requestsmap_l, exception_handler = request_exception_handler)
        responses_s = grequests.map(requestsmap_s, exception_handler = request_exception_handler)

        for res_l, res_s in zip(responses_l, responses_s):
            if res_l and res_l.ok:
                if res_s and res_s.ok:
                    content  = safe_decode(res_l.content)
                    lines    = content.split("\n")
                    proxies  = []

                    content  = safe_decode(res_s.content)
                    statuses = content.split("\n")

                    status_map = _build_status_map(statuses)

                    for line in lines:
                        output = proxy_to_dict(line, db_cast = True)
                        if output:
                            output["status"] = status_map.get(output["ip"])
                            proxies.append(output)

                    if proxies:
                        _save_proxies(proxies)
                else:
                    logger.warn("Unable to load URL %s: %s" % (res_s.url if res_s else "", res_s))
            else:
                logger.warn("Unable to load URL %s: %s" % (res_l.url if res_l else "", res_l))

        write(cache_path, "\n".join(hash_chunk), append = True)

    # save, commit and release
    logger.info("Commiting Latest Proxy List...")

    with make_temp_dir() as dir_path:
        repo = osp.join(dir_path, "proxy-list")

        github_username     = getenv("JOBS_GITHUB_USERNAME",    raise_err = True)
        github_oauth_token  = getenv("JOBS_GITHUB_OAUTH_TOKEN", raise_err = True)

        popen("git clone https://%s:%s@github.com/achillesrasquinha/proxy-list.git %s" % 
            (github_username, github_oauth_token, repo), cwd = dir_path)

        popen("git remote -vv", cwd = repo)

        proxy_path = osp.join(repo, "proxies.txt")

        with open(proxy_path, "w") as f:
            for row in connection.query("SELECT * FROM `tabProxies`"):
                proxy = proxy_to_str(row)

                f.write(proxy)
                f.write("\n")

        write(proxy_path, strip(read(proxy_path))) # remove trailing line.

        popen("git add %s" % proxy_path, cwd = repo)
        commit_message = "Update Proxy List: %s" % get_timestamp_str()
        popen("git commit --allow-empty -m '%s'" % commit_message, cwd = repo)

        popen("git push origin master", cwd = repo)

        logger.info("Proxy List upto date.")