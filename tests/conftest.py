# imports - standard imports
import sys, os, os.path as osp

def pardir(fname, level = 1):
    for _ in range(level):
        fname = osp.dirname(fname)
    return fname

PATH         = dict()
PATH["BASE"] = pardir(__file__, 2)

sys.path.append(PATH["BASE"])