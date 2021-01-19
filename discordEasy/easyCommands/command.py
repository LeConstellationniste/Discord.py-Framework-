from inspect import isfunction, signature

import discord

from ..errors import CommandError, MissingArgumentsError, DiscordTypeError
from .. import utils

class Command:
	def __init__(self, _function, name: str = None, aliases: list = [], types_options: list = []):
		self.name = name
		self.aliases = list(aliases)
		self.types_options = types_options
		if isfunction(_function):
			self._fct = _function
			self.nb_args = len(signature(self._fct).parameters) - 1  # -1 to not take Message argument
		else:
			raise TypeError(f"_function must be a function, not a {type(_function)}")

	def check_name(self, name: str):
		if isinstance(name, str):
			return name == self.name or name in self.aliases
		raise TypeError(f"`name` must be a str, not {type(name)}")

	def execute(self, *args):
		try:
			new_args = [args[0]] + utils.convert_list_str(list(args[1:]), self.types_options)
		except ValueError as e:
			raise DiscordTypeError(e, self)
		except TypeError as e:
			raise MissingArgumentsError(e, self)

		if len(new_args) - 1 < self.nb_args:
			raise MissingArgumentsError(TypeError("Missing 1 or more required positional argument"), self)

		try:
			return self._fct(*new_args)

		except Exception as e:
			raise CommandError(e, self)
