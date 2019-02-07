# pylint: disable=E0602

import sys
import os.path as osp
import glob
import io

from setuptools import setup, find_packages

import pip

try:
    from pip._internal.req import parse_requirements # pip 10
except ImportError:
    from pip.req           import parse_requirements # pip 9

# globals
PACKAGE     = "pipupgrade"
SRCDIR      = "src"

def isdef(var):
    return var in globals()

def read(path, encoding = None):
    content = None
    
    with io.open(path, encoding = encoding) as f:
        content = f.read()

    return content

def get_package_info():
    attr = osp.abspath(osp.join(SRCDIR, PACKAGE, "__attr__.py"))
    info = dict(__file__ = attr) # HACK
    
    with open(attr) as f:
        content = f.read()
        exec(content, info)

    return info

def get_dependencies(type_ = None):
    path         = osp.realpath("requirements.txt")
    requirements = [str(ir.req) for ir in parse_requirements(path, session = "hack")]

    if type_ == "development":
        path         = osp.realpath("requirements-dev.txt")
        requirements = [
            str(ir.req) for ir in parse_requirements(path, session = "hack")
                if str(ir.req) not in requirements
        ]
    
    return requirements

PKGINFO    = get_package_info()

setup(
    name                 = PKGINFO["__name__"],
    version              = PKGINFO["__version__"],
    url                  = PKGINFO["__url__"],
    author               = PKGINFO["__author__"],
    author_email         = PKGINFO["__email__"],
    description          = PKGINFO["__description__"],
    long_description     = read("README.md", encoding = "utf8"),
    long_description_content_type = "text/markdown",
    license              = PKGINFO["__license__"],
    keywords             = " ".join(PKGINFO["__keywords__"]),
    packages             = find_packages(where = SRCDIR),
    package_dir          = { "": SRCDIR },
    zip_safe             = False,
    entry_points         = {
        "console_scripts": [
            "%s = %s.__main__:main" % (
                PKGINFO["__command__"] if hasattr(PKGINFO, "__command__") else PKGINFO["__name__"],
                PACKAGE
            )
        ]
    },
    
    install_requires     = get_dependencies(type_ = "production"),
    extras_require       = dict(
        dev = get_dependencies(type_ = "development")
    ),
    include_package_data = True,
    classifiers          = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ]
)
