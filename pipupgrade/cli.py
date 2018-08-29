_ACCEPTABLE_YES = ("", "y", "Y")

BOLD  = "\033[0;1m"
GREEN = "\033[0;32m"
CLEAR = "\033[0m"

def confirm(query):
    query  = "{} [Y/n]: ".format(query)
    output = input(query)

    return output in _ACCEPTABLE_YES

def format(string, type_):
    string = "{}{}{}".format(type_, string, CLEAR)
    return string

def echo(string, nl = True):
    print(string, end = "\n" if nl else "")