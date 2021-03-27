# functions to manipulate str
from typing import Iterable


def replace_multiple(_str: str, to_replace: Iterable[str], new_char: str = "") -> str:
	for c in to_replace:
		_str = _str.replace(c, new_char)
	return _str


def list_to_str(_list: Iterable) -> str:
	return ", ".join(_list)
