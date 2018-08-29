import sys
import os.path as osp

from   setuptools import setup, find_packages

import pip

try:
    from pip._internal.req import parse_requirements # pip 10
except ImportError:
    from pip.req           import parse_requirements # pip 9

# globals
PROJECT_DIRNAME = "pipupgrade"
COMMAND_NAME    = "pipupgrade"
ENVIRONMENT     = "production" if sys.argv[1] == "install" else "development"

def isdef(var):
    return var in globals()

with open(osp.join(PROJECT_DIRNAME if isdef("PROJECT_DIRNAME") else __name__, "__attr__.py")) as f:
    content = f.read()
    exec(content)

def get_dependencies(type_ = None):
    path         = osp.abspath("requirements{type_}.txt".format(
        type_    = "-dev" if type_ == "development" else ""
    ))
    requirements = [str(ir.req) for ir in parse_requirements(path, session = "hack")]
    
    return requirements

def read(path):
    path = osp.abspath(path)
    
    with open(path) as f:
        content = f.read()
    return content

setup(
    name                 = __name__,
    version              = __version__,
    url                  = __url__,
    author               = __author__,
    author_email         = __email__,
    description          = __description__,
    long_description     = read("README.md"),
    license              = __license__,
    keywords             = " ".join(__keywords__),
    packages             = find_packages(),
    entry_points         = {
        "console_scripts": [
            "{name} = {project}.__main__:main".format(
                name    = COMMAND_NAME    if isdef("COMMAND_NAME")    else __name__,
                project = PROJECT_DIRNAME if isdef("PROJECT_DIRNAME") else __name__
            )
        ]
    },
    install_requires     = get_dependencies(type_ = ENVIRONMENT if isdef(ENVIRONMENT) else None),
    include_package_data = True,
    classifiers          = (
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
    )
)