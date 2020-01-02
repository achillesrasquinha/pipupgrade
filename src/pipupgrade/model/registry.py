# imports - standard imports
import re

# imports - module imports
from pipupgrade.model.package   import Package, _get_pip_info
from pipupgrade                 import _pip, parallel
from pipupgrade.util.types      import flatten
from pipupgrade.util.array      import compact
from pipupgrade.util.string     import kebab_case, lower
from pipupgrade._compat		    import iteritems, iterkeys, itervalues
from pipupgrade.tree            import Node as TreeNode

_PACKAGE_INFO_DICT = dict()

def _build_packages_info_dict(packages, pip_exec = None):
    names       = list(map(lower, packages))
    details     = _get_pip_info(*names, pip_exec = pip_exec)

    for name, detail in iteritems(details):
        name = lower(name)
        
        if not name in _PACKAGE_INFO_DICT:
            _PACKAGE_INFO_DICT[name] = compact(
                map(lower, detail["requires"].split(", "))
            )
    
    packages    = list(filter(lambda x: x not in _PACKAGE_INFO_DICT, 
        flatten(itervalues(_PACKAGE_INFO_DICT))
    ))

    if packages:
        _build_packages_info_dict(packages, pip_exec = pip_exec)

def _get_dependency_tree_for_package(package, pip_exec = None):
    tree                    = TreeNode(package)

    name                    = lower(package.name)
    dependencies            = [Package(p, pip_exec = pip_exec) \
        for p in _PACKAGE_INFO_DICT[name]]

    for dependency in dependencies:
        child = _get_dependency_tree_for_package(dependency)
        tree.add_child(child)

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

        args        = { "sync": sync }

        if installed:
            args["pip_exec"] = source

        self.packages  = [Package(p, **args)
            for p in packages
        ]

        self.installed = installed
        
        if installed and dependencies:
            self._build_dependency_tree_for_packages()

    def _build_dependency_tree_for_packages(self):
        names        = [p.name for p in self.packages]
        _build_packages_info_dict(names, pip_exec = self.source)

        for package in self.packages:
            package.dependencies = _get_dependency_tree_for_package(package,
                pip_exec = self.source
            )