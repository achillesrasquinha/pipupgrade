import os.path as osp
import gzip
from   datetime import datetime as dt
import json
import pkg_resources

from pipupgrade.__attr__ import __name__ as NAME

from bpyutils._compat   import iterkeys
from bpyutils.log       import get_logger
from bpyutils.config    import PATH, Settings
from bpyutils           import request as req
from pipupgrade.model.package import Package

from semver import Version, VersionRange, parse_constraint

from mixology.constraint     import Constraint
from mixology.package_source import PackageSource as BasePackageSource
from mixology.range          import Range
from mixology.union          import Union

logger   = get_logger(name = NAME)
settings = Settings()

def populate_db():
    dt_now = dt.now()

    logger.info("Populating DB...")

    path_gzip = osp.join(PATH["CACHE"], "dependencies.json.gz")
    path_uzip = osp.join(PATH["CACHE"], "dependencies.json")

    refresh   = False

    if not osp.exists(path_gzip):
        refresh = True
    else:
        time_modified = dt.fromtimestamp( osp.getmtime(path_gzip) )
        cache_seconds = settings.get("cache_timeout")
        delta_seconds = (time_modified - dt_now).total_seconds()

        if delta_seconds > cache_seconds:
            refresh = True

    if refresh:
        logger.info("Fetching Dependency Graph...")

        response = req.get("https://github.com/achillesrasquinha/pipupgrade/blob/master/data/dependencies.json.gz?raw=true",
            stream = True)

        if response.ok:
            with open(path_gzip, "wb") as f:
                for content in response.iter_content(chunk_size = 1024):
                    f.write(content)
        else:
            response.raise_for_status()

        with gzip.open(path_gzip, "rb") as rf:
            with open(path_uzip, "wb") as wf:
                content = rf.read()
                wf.write(content)

_DEPENDENCIES = {}

def _parse_dependencies(deps):
    return [ pkg_resources.Requirement.parse(dep) for dep in deps ]

def get_meta(package, version):
    global _DEPENDENCIES
    
    if not _DEPENDENCIES:
        path_dependencies = osp.join(PATH["CACHE"], "dependencies.json")

        with open(path_dependencies) as f:
            _DEPENDENCIES = json.load(f)

    data = _DEPENDENCIES.get(package.name, {})

    dependencies = _parse_dependencies(data.get(version) or [])
    
    return {
        "releases": list(iterkeys(data)),
        "dependencies": dependencies
    }

class Dependency:
    def __init__(self, package, constraint = None):
        self.name               = package.name
        self.constraint         = parse_constraint(constraint or "*")
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

    def add(self, name, extras, version, deps = None):
        version = Version.parse(version)
        
        if name not in self._packages:
            self._packages[name] = { extras: {} }
        if extras not in self._packages[name]:
            self._packages[name][extras] = {}

        if version in self._packages[name][extras] and not (
            deps is None or self._packages[name][extras][version] is None
        ):
            raise ValueError("{} ({}) already exists".format(name, version))

        if deps is None:
            self._packages[name][extras][version] = None
        else:
            dependencies = []
            for dep in deps:
                dependencies.append(Dependency(dep))

            self._packages[name][extras][version] = dependencies

    def root_dep(self, package, constraint):
        logger.info("Adding Root Dependency with Constraint: %s, %s" % (package, constraint))

        dependency   = Dependency(package, constraint)
        self._root_dependencies.append(dependency)

        self.discover_and_add(package, constraint)

    def discover_and_add(self, package, constraint = None):
        # discover and add
        metadata     = get_meta(package, constraint)
        logger.info("Releases for package %s found: %s" % (package, metadata["releases"]))

        for release in metadata["releases"]:
            self.add(package.name, package.extras, release)

        deps = []
        logger.info("Adding Dependencies for package %s: %s" % (package, metadata["dependencies"]))
        for dependency in metadata["dependencies"]:
            deps.append(Package(dependency.name))

        self.add(package.name, package.extras, constraint, deps = deps)

    def _versions_for(self, package, constraint = None):
        package = Package(package)

        extras  = package.extras

        if package not in self._packages or extras not in self._packages[package]:
            self.discover_and_add(package, constraint)

        if package not in self._packages:
            return [ ]

        versions = [ ]
        for version in iterkeys(self._packages[package][extras]):
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