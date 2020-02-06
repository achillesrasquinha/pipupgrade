# imports - compatibility imports
from pipupgrade._compat import cmp

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
        patch = None
    ):
        self._major = major
        self._minor = minor
        self._patch = patch

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def patch(self):
        return self._patch

def parse(version):
    match   = _REGEX_SEMVER.match(version)
    if not match:
        raise ValueError("{} is not a valid Semantic Version string".format(version))

    version = match.groupdict()

    version["major"] = int(version["major"])
    version["minor"] = int(version["minor"])
    version["patch"] = int(version["patch"])

    version          = Version(
        major = version["major"],
        minor = version["minor"],
        patch = version["patch"]
    )

    return version

def difference(a, b):
    va = parse(a)
    vb = parse(b)

    if a != b:
        for key in ["major", "minor", "patch"]:
            if cmp(va.get(key), vb.get(key)):
                return key
        
        raise NotImplementedError("Unknown difference between {} and {}".format(a, b))
    else:
        return None