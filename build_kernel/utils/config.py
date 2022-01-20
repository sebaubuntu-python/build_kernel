from build_kernel import config

def get_config(name: str, default=None):
	"""Get a property from config.py."""
	if not '.' in name:
		if name in config:
			value = config[name]
		else:
			value = default
	else:
		value = config
		for key in name.split('.'):
			if not key in value:
				value = default
				break
			value = value[key]

	if value == "":
		return default

	return value
