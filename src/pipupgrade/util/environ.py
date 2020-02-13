# imports - standard imports
import os

# imports - module imports
import pipupgrade
from   pipupgrade.util.types 	import auto_typecast
from   pipupgrade._compat		import string_types

PREFIX = "%s" % pipupgrade.__name__.upper()

def getenvvar(name, prefix = PREFIX, seperator = "_"):
	if not prefix:
		prefix	  = ""
		seperator = ""

	envvar = "%s%s%s" % (prefix, seperator, name)
	return envvar

def getenv(name, default = None, cast = True, prefix = PREFIX, seperator = "_", raise_err = False):
    envvar = getenvvar(name, prefix = prefix, seperator = seperator)

    if not envvar in list(os.environ) and raise_err:
        raise KeyError("Environment Variable %s not found." % envvar)

    value  = os.getenv(envvar, default)
    value  = auto_typecast(value) if cast else value

    return value

def value_to_envval(value):
	"""
	Convert python types to environment values
	"""

	if not isinstance(value, string_types):
		if   value == True:
			value = "true"
		elif value == False:
			value = "false"
		elif isinstance(value, int):
			value = str(value)
		else:
			raise TypeError("Unknown parameter type %s with value %r" % (value, type(value)))

	return value