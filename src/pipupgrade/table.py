# imports - compatibility imports
from pipupgrade._compat     import zip_longest

# imports - module imports
from pipupgrade.util.string import strip_ansi

def _sanitize_string(string):
    """
    Helper for tabulate to sanitize strings.
    """
    string = strip_ansi(string)
    return string

def tabulate(rows):
    # Shamelessly taken from: https://git.io/fARTL (pip)
    # Also: https://git.io/fARTY (yarn)
    # Yo, WTF is wrong with git.io and its "fart" filled short urls?

    sizes  = [0] * max(len(x) for x in rows)
    for row in rows:
        sizes = [max(s, len(str(_sanitize_string(c if c else "")))) for s, c in zip_longest(sizes, row)]

    result = [ ]
    for row in rows:
        display = " ".join([str(c) + " " * (s - len(_sanitize_string(c if c else ""))) if c is not None else ""
                            for s, c in zip_longest(sizes, row)])
        result.append(display)

    return result, sizes

class Table:
    def __init__(self, header = None):
        self.rows   = [ ]
        self.header = header or [ ]

    @property
    def empty(self):
        _empty = len(self) == 0
        return _empty

    def insert(self, row):
        self.rows.append(row)

    def render(self, header = True):
        string = ""

        _rows  = self.rows[:]
        
        if header and self.header:
            _rows.insert(0, self.header)

        if _rows:
            tabulated, sizes = tabulate(_rows)
            
            # divider
            if header:
                tabulated.insert(1, " ".join(map(lambda x: "-" * x, sizes)))

            string  = "\n".join(tabulated)

        return string
    
    def __len__(self):
        length = len(self.rows)
        return length