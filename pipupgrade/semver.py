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

def parse(version):
    match   = _REGEX_SEMVER.match(version)
    if not match:
        raise ValueError("{} is not a valid Semantic Version string".format(version))

    version = match.groupdict()

    version["major"] = int(version["major"])
    version["minor"] = int(version["minor"])
    version["patch"] = int(version["patch"])

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