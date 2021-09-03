# imports - compatibility imports
from __future__ import absolute_import

# imports - standard imports
import re
from   functools import partial

# imports - module imports
from pipupgrade.__attr__ import __name__ as NAME

from pipupgrade.model.package import Package, _get_pip_info
from bpyutils.util.array      import compact
from bpyutils._compat		  import iteritems
from bpyutils.tree            import Node as TreeNode
from bpyutils.log             import get_logger

from bpyutils import parallel

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
    data    = dict(
        name    = name,
        version = _INFO_DICT[name]["version"]
    )
    package = Package(data, sync = sync)

    return package

def _get_dependency_tree_for_package(package, parent = None, sync = False,
    jobs = 1, depth = None, level = 0):
    if package.name not in _TREE_DICT:
        logger.info("Building dependency tree for package: %s..." % package)

        tree = TreeNode(package, parent = parent)

        dependencies = [ ]

        with parallel.no_daemon_pool(processes = jobs) as pool:
            dependencies = pool.imap_unordered(
                partial(
                    _create_package, **{
                        "sync": sync
                    }
                ),
                _INFO_DICT[package.name]["dependencies"]
            )

        if not depth or depth != level:
            with parallel.no_daemon_pool(processes = jobs) as pool:
                children = pool.imap_unordered(
                    partial(
                        _get_dependency_tree_for_package, **{
                            "parent": tree, "depth": depth, "level": level + 1
                        }
                    ),
                    dependencies
                )

                if children:
                    tree.add_children(*children)

        _TREE_DICT[package.name] = tree
    else:
        logger.info("Using cached dependency tree for package: %s." % package)

    tree = _TREE_DICT[package.name]
    tree.parent = parent

    return tree

class Registry(object):
    def __init__(self,
        source,
        packages                = [ ],
        installed               = False,
        sync                    = False,
        build_dependency_tree   = False,
        resolve                 = False,
        latest                  = False,
        jobs                    = 1
    ):
        self.source     = source

        args = { "sync": sync }

        if installed:
            args["pip_exec"] = source
        
        self.installed  = installed

        self._packages  = [ ]

        with parallel.no_daemon_pool(processes = jobs) as pool:
            for package in pool.imap_unordered(partial(Package, **args), packages):
                self._packages.append(package)

        if installed and build_dependency_tree and self._packages:
            self._build_dependency_tree_for_packages(sync = sync, jobs = jobs)

        if resolve: # --format tree overtakes --resolve
            # by default, attempt latest resolution

            # build shallow dependency list
            # if installed:
            #     self._build_dependency_tree_for_packages(sync = sync, jobs = jobs, depth = 1)

            logger.info("Resolving Packages %s...", self._packages)

            from mixology.version_solver import VersionSolver
            from pipupgrade.pubgrub      import PackageSource

            source = PackageSource()
            for package in self._packages:
                source.root_dep(package, package.latest_version)

            solver = VersionSolver(source)
            result = solver.solve()

            logger.info("Resolution Result: %s", result.decisions)

    @property
    def packages(self):
        packages = getattr(self, "_packages", [ ])
        return sorted(packages, key = lambda x: x.name.lower())

    def _build_dependency_tree_for_packages(self, sync = False, jobs = 1, depth = None):
        names = [p.name for p in self.packages]
        _build_packages_info_dict(names, pip_exec = self.source)

        for package in self.packages:
            package.dependency_tree = _get_dependency_tree_for_package(package,
                sync = sync, jobs = 1, depth = depth)