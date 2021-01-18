import discord

from ..errors import ArgumentsError

class Command:
	def __init__(self, _function, name: str = None, aliases: list = []):
		self.name = name
		self.aliases = list(aliases)
		self._fct = _function

	def check_name(self, name: str):
		if isinstance(name, str):
			return name == self.name or name in self.aliases
		raise TypeError(f"`name` must be a str, not {type(name)}")

	def execute(self, *args):
		try:
			return self._fct(*args)
		except TypeError as e:
			raise ArgumentsError(e)

