from mixology.package_source import PackageSource as BasePackageSource

from pipupgrade import semver

class Dependency:
    pass

class PackageSource(BasePackageSource):
    def __init__(self, *args, **kwargs):
        self._root_version  = semver.parse("0.0.0")

        self.super          = super(PackageSource, self)
        self.super.__init__(*args, **kwargs)

    @property
    def root_version(self):
        return self._root_version

    def root_dep(self, package):
        print(package)

    def dependencies_for(self, package, version):
        pass