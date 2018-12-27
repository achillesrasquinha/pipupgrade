def value_to_envval(value):
	"""
	Convert python types to environment values
	"""

	if not isinstance(value, str):
		if   value == True:
			value = "true"
		elif value == False:
			value = "false"
		elif isinstance(value, int):
			value = str(value)
		else:
			raise TypeError("Unknown parameter type %s with value %r" % (value, type(value)))

	return value