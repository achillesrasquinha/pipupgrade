# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import os.path as osp
import json

# imports - module imports
from   pipupgrade.util.system import read as fread, makedirs

def read(fname):
    content = fread(fname) or r"{}"
    json_   = json.loads(content)

    return json_

def write(fname, dict_, force = False, indent = 2):
    if not osp.exists(fname) or force:
        fpath = osp.dirname(fname)
        makedirs(fpath, exist_ok = True)

        with open(fname, "w") as f:
            json.dump(dict_, f, indent = indent)

def update(fname, dict_):
    json_ = read(fname)
    json_.update(dict_)

    write(fname, json_, force = True)