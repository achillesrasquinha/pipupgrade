# imports - standard imports
import os.path as osp

def read(fname):
    with open(fname) as f:
        data = f.read()
    return data

def write(fname, data = None, force = False):
    if not osp.exists(fname) or force:
        with open(fname, "w") as f:
            if data:
                f.write(data)