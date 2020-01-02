# imports - standard imports
import re

# imports - module imports
from pipupgrade.model.package   import Package
from pipupgrade                 import _pip
from pipupgrade.util.types      import flatten
from pipupgrade.util.array      import compact
from pipupgrade.util.string     import kebab_case, lower
from pipupgrade._compat		    import iteritems, iterkeys, itervalues

_PACKAGE_INFO_DICT = dict()

def _build_packages_info_dict(packages, pip_exec = None):
    names       = list(map(lower, packages))
    _, out, err = _pip.call("show", *names, output = True, pip_exec = pip_exec)
    results     = out.split("---")

    for result in results:
        detail  = dict((kebab_case(k), v) \
            for k, v in \
                iteritems(
                    dict([(s + [""]) if len(s) == 1 else s
                        for s in [re.split(':\s?', o, maxsplit = 1) \
                            for o in result.split("\n")]]
                    )
                )
        )

        name    = lower(detail["name"])
        
        if not name in _PACKAGE_INFO_DICT:
            _PACKAGE_INFO_DICT[name] = compact(
                map(lower, detail["requires"].split(", "))
            )
    
    packages    = list(filter(lambda x: x not in _PACKAGE_INFO_DICT, 
        flatten(itervalues(_PACKAGE_INFO_DICT))
    ))

    if packages:
        _build_packages_info_dict(packages, pip_exec = pip_exec)

def _build_dependency_tree_for_packages(packages):
    for package in packages:
        self.pack

class Registry:
    def __init__(self,
        source,
        packages        = [ ],
        installed       = False,
        sync            = False,
        dependencies    = False
    ):
        self.source = source

        self.packages  = [Package(p, sync = sync)
            for p in packages
        ]

        self.installed = installed
        
        if installed and dependencies:
            self._build_dependency_tree_for_packages()

    def _build_dependency_tree_for_packages(self):
        names = [p.name for p in self.packages]
        _build_packages_info_dict(names, pip_exec = self.source)
        _build_dependency_tree_for_packages(self.packages)