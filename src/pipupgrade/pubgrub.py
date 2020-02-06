from mixology.package_source import PackageSource as BasePackageSource

from pipupgrade import semver

class Dependency:
    pass

class PackageSource(BasePackageSource):
    def __init__(self):
        self._root_version = semver.parse("0.0.0")

    @property
    def root_version(self):
        return self._root_version