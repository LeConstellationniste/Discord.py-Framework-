# functions to manipulate str


def convert_list_str(str_list: list, types: list):
	new_list = []
	if len(types) > 0 and len(types) == len(str_list):
		for _str, _type in zip(str_list, types):
			new_list.append(_type(_str))  # ValueError can be raised

	elif len(types) > 0 and len(str_list) < len(types):
		raise TypeError("Missing 1 or more required positional argument")

	else:
		new_list = str_list

	return new_list


def replace_multiple(_str: str, to_replace: list, new_char: str = ""):
	for c in to_replace:
		_str = _str.replace(c, new_char)
	return _str
