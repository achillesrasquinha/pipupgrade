# imports - standard imports
import re

_REGEX_ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

def strip(string):
    string = string.lstrip()
    string = string.rstrip()

    return string 

def strip_ansi(string):
    string = _REGEX_ANSI_ESCAPE.sub("", string)
    return string

def pluralize(string, count = 1):
    # A very shitty pluralizer
    if not string.endswith("s"):
        if count > 1:
            string += "s"
    
    return string

def kebab_case(string, delimiter = " "):
    words = string.replace(delimiter, " ").split()
    kebab = "-".join([word.lower() for word in words])
    
    return kebab

def safe_encode(obj, encoding = "utf-8"):
    try:
        obj = obj.encode(encoding)
    except (AttributeError, UnicodeEncodeError):
        pass
    
    return obj