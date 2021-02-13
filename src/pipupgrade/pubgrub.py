from pipupgrade._compat import iteritems, iterkeys

from semver import Version, VersionRange, parse_constraint

from mixology.constraint     import Constraint
from mixology.package_source import PackageSource as BasePackageSource
from mixology.range          import Range
from mixology.union          import Union

class Dependency:
    def __init__(self, package, constraint):
        self.name               = package.name
        self.constraint         = parse_constraint(constraint)
        self.pretty_constraint  = constraint

    def __str__(self):
        return self.pretty_constraint

class PackageSource(BasePackageSource):
    def __init__(self, *args, **kwargs):
        self._root_version      = Version.parse("0.0.0")
        self._root_dependencies = [ ]
        self._packages          = { }

        self.super = super(PackageSource, self)
        self.super.__init__(*args, **kwargs)

    @property
    def root_version(self):
        return self._root_version

    def add(self, name, version, deps = None):
        if deps is None:
            deps = { }

        version = Version.parse(version)
        if name not in self._packages:
            self._packages[name] = { }

        if version in self._packages[name]:
            raise ValueError("{} ({}) already exists".format(name, version))

        dependencies = [ ]
        for dep_name, spec in iteritems(deps):
            dependencies.append(Dependency(dep_name, spec))

        self._packages[name][version] = dependencies

    def root_dep(self, package, constraint):
        dependency = Dependency(package, constraint)
        self._root_dependencies.append(dependency)

        # for release in package.releases:
        #     self.add(package.name, release)

        # self.add(package.name, package.current_version, package.dependency_tree.children)

    def _versions_for(self, package, constraint):
        if package not in self._packages:
            return [ ]

        versions = [ ]
        for version in iterkeys(self._packages[package]):
            if not constraint or constraint.allows_any(
                Range(version, version, True, True)
            ):
                versions.append(version)

        return sorted(versions, reverse = True)

    def dependencies_for(self, package, version):
        if package == self.root:
            return self._root_dependencies
        return self._packages[package][version]

    def convert_dependency(self, dependency):
        if isinstance(dependency.constraint, VersionRange):
            constraint = Range(
                dependency.constraint.min,
                dependency.constraint.max,
                dependency.constraint.include_min,
                dependency.constraint.include_max,
                dependency.pretty_constraint,
            )
        else:
            ranges = [
                Range(
                    _range.min,
                    _range.max,
                    _range.include_min,
                    _range.include_max,
                    str(_range),
                )
                for _range in dependency.constraint.ranges
            ]
            constraint = Union.of(ranges)

        return Constraint(dependency.name, constraint)