# imports - compatibility imports
from bpyutils._compat import cmp

# imports - standard imports
import re

_REGEX_SEMVER = re.compile(r"""
    ^
    (?P<major>(?:0|[1-9][0-9]*))
    \.
    (?P<minor>(?:0|[1-9][0-9]*))
    \.
    (?P<patch>(?:0|[1-9][0-9]*))
    (\-(?P<prerelease>
        (?:0|[1-9A-Za-z-][0-9A-Za-z-]*)
        (\.(?:0|[1-9A-Za-z-][0-9A-Za-z-]*))*
    ))?
    (\+(?P<build>
        [0-9A-Za-z-]+
        (\.[0-9A-Za-z-]+)*
    ))?
    $
    """, re.VERBOSE)

class Version:
    def __init__(self,
        major,
        minor = None,
        patch = None,
        prerelease = None,
        build = None
    ):
        self._major = major
        self._minor = minor
        self._patch = patch
        self._prerelease = prerelease
        self._build = build

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

    @property
    def prerelease(self):
        return self._prerelease

    @property
    def build(self):
        return self._build
    
    # backward compatibility
    def __getitem__(self, key):
        return getattr(self, key)

def parse(version):
    match   = _REGEX_SEMVER.match(version)
    if not match:
        raise ValueError("{} is not a valid Semantic Version string".format(version))

    version = match.groupdict()

    version = Version(
        major = int(version["major"]),
        minor = int(version["minor"]),
        patch = int(version["patch"]),
        prerelease = version["prerelease"],
        build = version["build"]
    )

    return version

def difference(a, b):
    va = parse(a)
    vb = parse(b)

    if a != b:
        for key in ("major", "minor", "patch"):
            if cmp(va[key], vb[key]):
                return key
        
        raise NotImplementedError("Unknown difference between {} and {}".format(a, b))
    else:
        return None