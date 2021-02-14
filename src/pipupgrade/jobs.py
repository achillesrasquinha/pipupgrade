import requests as req
from bs4 import BeautifulSoup

from pipupgrade.db          import get_connection
from pipupgrade.util.string import safe_decode

BASE_INDEX_URL = "https://pypi.org/simple"

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
                print(versions)
                break
            else:
                res.raise_for_status()
    else:
        res.raise_for_status()

def build_proxy_list():
    pass