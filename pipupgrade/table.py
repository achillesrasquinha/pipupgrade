# imports - compatibility imports
from pipupgrade._compat import zip_longest

# imports - standard imports
import re

# imports - module imports
from pipupgrade.util import get_if_empty

_REGEX_ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

def _strip_ansi(string):
    string = _REGEX_ANSI_ESCAPE.sub("", string)
    return string

def _sanitize(string):
    string = _strip_ansi(string)
    return string

def tabulate(rows):
    # https://github.com/pypa/pip/blob/404838a/src/pip/_internal/commands/list.py#L237

    sizes  = [0] * max(len(x) for x in rows)
    for row in rows:
        sizes = [max(s, len(str(_sanitize(c)))) for s, c in zip_longest(sizes, row)]

    result = [ ]
    for row in rows:
        display = " ".join([str(c) + " " * (s - len(_sanitize(c))) if c is not None else ""
                            for s, c in zip_longest(sizes, row)])
        result.append(display)

    return result, sizes

class Table:
    def __init__(self, header = None):
        self.rows   = [ ]
        self.header = get_if_empty(header, [ ])

    @property
    def empty(self):
        _empty = len(self.rows) == 0
        return _empty

    def insert(self, row):
        self.rows.append(row)

    def render(self):
        string = ""

        _rows  = self.rows
        
        if self.header:
            _rows.insert(0, self.header)

        if _rows:
            tabulated, sizes = tabulate(_rows)
            # divider
            tabulated.insert(1, " ".join(map(lambda x: "-" * x, sizes)))

            string  = "\n".join(tabulated)

        return string