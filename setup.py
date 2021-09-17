# pylint: disable=E0602

import sys
import os.path as osp
import glob
import io
import shutil

from setuptools import setup, find_packages

from setuptools.command.develop import develop
from setuptools.command.install import install

# import pip

# try:
#     from pip._internal.req import parse_requirements # pip 10
# except ImportError:
#     from pip.req           import parse_requirements # pip 9

# globals
PACKAGE     = "pipupgrade"
SRCDIR      = "src"

# A very awful patch for parse_requirements from pip
def parse_requirements(filename, session = None):
    class FakeRequirement:
        def __init__(self, name):
            self.req = name
            
    def sanitize_line(line):
        line = line.strip()
        return line

    def check_line(line):
        return line and not line.startswith("#")

    return [
        FakeRequirement(sanitize_line(line)) for line in open(filename) if check_line(line)
    ]

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


def remove_cache():
    userdir = osp.expanduser("~")
    pkgname = PKGINFO["__name__"]

    paths = [
        osp.join(userdir, ".%s" % pkgname), # backward-compatibility
        osp.join(userdir, ".config", pkgname)
    ]

    for path in paths:
        if osp.exists(path):
            shutil.rmtree(path)

class DevelopCommand(develop):
    def run(self):
        develop.run(self)
        remove_cache()

class InstallCommand(install):
    def run(self):
        install.run(self)
        remove_cache()
        
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    cmdclass = {
        "install": InstallCommand,
        "develop": DevelopCommand
    }
)