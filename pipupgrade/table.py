# imports - module imports
from pipupgrade.util import get_if_empty

class Table:
    def __init__(self):
        self.rows   = [ ]
        self.header = None

    def insert(self, row):
        self.rows.append(row)

    def render(self):
        string  = ""

        header  = get_if_empty(self.header, [ ])
        format_ = "{:>" + offset + "}" * (len(header) + 1)

        return string