# functions to manipulate str


def replace_multiple(_str: str, to_replace: list, new_char: str = "") -> str:
	for c in to_replace:
		_str = _str.replace(c, new_char)
	return _str


def list_to_str(_list: list) -> str:
	return replace_multiple(str(_list), ["[", "]"], "")
