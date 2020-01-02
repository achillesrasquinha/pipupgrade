# imports - standard imports
import re
from   functools import partial

# imports - module imports
from pipupgrade.model.package   import Package, _get_pip_info
from pipupgrade                 import _pip, parallel
from pipupgrade.util.types      import flatten
from pipupgrade.util.array      import compact
from pipupgrade.util.string     import kebab_case, lower
from pipupgrade._compat		    import iteritems, iterkeys, itervalues
from pipupgrade.tree            import Node as TreeNode

_DEPENDENCY_DICT = dict()
_VERSION_DICT    = dict()

def _build_packages_info_dict(packages, pip_exec = None):
    details         = _get_pip_info(*packages, pip_exec = pip_exec)

    requirements    = [ ]

    for name, detail in iteritems(details):
        if not name in _DEPENDENCY_DICT:
            _VERSION_DICT[name]    = detail["version"]
            _DEPENDENCY_DICT[name] = compact(
                map(lower, detail["requires"].split(", "))
            )

            for requirement in _DEPENDENCY_DICT[name]:
                if requirement not in requirements:
                    requirements.append(requirement)

    if requirements:
        _build_packages_info_dict(requirements, pip_exec = pip_exec)

def _build_package(name, sync = False):
    package = Package(name, sync = sync)
    package.current_version = _VERSION_DICT[name]
    
    return package

def _get_dependency_tree_for_package(package, sync = False):
    tree                    = TreeNode(package)

    dependencies            = [ ]
    
    with parallel.no_daemon_pool() as pool:
        dependencies = pool.map(
            partial(
                _build_package, **{
                    "sync": sync
                }
            ),
            _DEPENDENCY_DICT[package.name]
        )

    with parallel.no_daemon_pool() as pool:
        children = pool.map(_get_dependency_tree_for_package, dependencies)
        
        if children:
            tree.add_children(*children)

    return tree

class Registry:
    def __init__(self,
        source,
        packages        = [ ],
        installed       = False,
        sync            = False,
        dependencies    = False
    ):
        self.source = source

        self.sync   = sync

        args        = { "sync": sync }

        if installed:
            args["pip_exec"] = source
        
        with parallel.no_daemon_pool() as pool:
            self.packages = pool.map(partial(Package, **args), packages)

        self.installed = installed
        
        if installed and dependencies:
            self._build_dependency_tree_for_packages()

    def _build_dependency_tree_for_packages(self):
        names = [p.name for p in self.packages]
        _build_packages_info_dict(names, pip_exec = self.source)

        for package in self.packages:
            package.dependencies = _get_dependency_tree_for_package(package,
                sync = self.sync
            )