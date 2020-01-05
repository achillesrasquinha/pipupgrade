# imports - standard imports
import sys, os, os.path as osp
import logging

def pardir(fname, level = 1):
    fname = osp.realpath(fname)

    for _ in range(level):
        fname = osp.dirname(fname)
    return fname

PATH          = dict()
PATH["BASE"]  = pardir(__file__, 2)
PATH["TESTS"] = osp.join(PATH["BASE"], "tests")

sys.path.append(
    osp.join(PATH["TESTS"], "helpers")
)