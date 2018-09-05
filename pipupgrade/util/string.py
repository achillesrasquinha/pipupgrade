# imports - standard imports
import re

_REGEX_ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

def strip_ansi(string):
    string = _REGEX_ANSI_ESCAPE.sub("", string)
    return string