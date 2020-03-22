# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import re
from   functools import partial, cmp_to_key

# imports - module imports
from pipupgrade.model.package   import Package, _get_pip_info
from pipupgrade                 import _pip, parallel
from pipupgrade.util.array      import compact, flatten
from pipupgrade.util.string     import kebab_case
from pipupgrade._compat		    import iteritems, iterkeys, itervalues
from pipupgrade.tree            import Node as TreeNode
from pipupgrade.log             import get_logger

logger = get_logger()

# cache package information
_INFO_DICT = dict()
# cache dependency trees
_TREE_DICT = dict()

def _build_packages_info_dict(packages, pip_exec = None):
    details         = _get_pip_info(*packages, pip_exec = pip_exec)

    requirements    = [ ]

    for name, detail in iteritems(details):
        if not name in _INFO_DICT:
            _INFO_DICT[name] = dict({
                     "version": detail["version"], 
                "dependencies": compact(detail["requires"].split(", "))
            })

            for requirement in _INFO_DICT[name]["dependencies"]:
                if requirement not in requirements:
                    requirements.append(requirement)

    if requirements:
        _build_packages_info_dict(requirements, pip_exec = pip_exec)

def _create_package(name, sync = False):
    data                    = dict(
        name    = name,
        version = _INFO_DICT[name]["version"]
    )
    package                 = Package(data, sync = sync)
    
    return package

def _get_dependency_tree_for_package(package, parent = None, sync = False,
    jobs = 1):
    if package.name not in _TREE_DICT:
        logger.info("Building dependency tree for package: %s..." % package)

        tree            = TreeNode(package, parent = parent)

        dependencies    = [ ]
        
        with parallel.no_daemon_pool(processes = jobs) as pool:
            dependencies = pool.imap_unordered(
                partial(
                    _create_package, **{
                        "sync": sync
                    }
                ),
                _INFO_DICT[package.name]["dependencies"]
            )

        with parallel.no_daemon_pool(processes = jobs) as pool:
            children = pool.imap_unordered(
                partial(
                    _get_dependency_tree_for_package, **{
                        "parent": tree
                    }
                ),
                dependencies
            )

            if children:
                tree.add_children(*children)

        _TREE_DICT[package.name] = tree
    else:
        logger.info("Using cached dependency tree for package: %s." % package)

    tree        = _TREE_DICT[package.name]
    tree.parent = parent

    return tree

class Registry(object):
    def __init__(self,
        source,
        packages                = [ ],
        installed               = False,
        sync                    = False,
        build_dependency_tree   = False,
        jobs                    = 1
    ):
        self.source     = source

        args            = { "sync": sync }

        if installed:
            args["pip_exec"] = source
        
        self._packages  = [ ]
        with parallel.no_daemon_pool(processes = jobs) as pool:
            for package in pool.imap_unordered(partial(Package, **args), packages):
                self._packages.append(package)

        self.installed  = installed
        
        if installed and build_dependency_tree and self._packages:
            self._build_dependency_tree_for_packages(sync = sync, jobs = jobs)

    @property
    def packages(self):
        packages = getattr(self, "_packages", [ ])
        return sorted(packages, key = lambda x: x.name.lower())

    def _build_dependency_tree_for_packages(self, sync = False, jobs = 1):
        names = [p.name for p in self.packages]
        _build_packages_info_dict(names, pip_exec = self.source)

        for package in self.packages:
            package.dependency_tree = _get_dependency_tree_for_package(package,
                sync = sync, jobs = 1)