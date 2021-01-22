from inspect import isfunction, isroutine, iscoroutine, signature

import discord

from .. import errors
from .. import utils

class Command:
	def __init__(self, _function, name: str = None, aliases: list = [], types_options: list = [], check=None):
		""" Arguments:
			* _function: the function to execute, it's the base of command
			* name: the name of command, if None, the name attribute of function is used. It's the name which is used in Discord to call the command.
			* aliases: a list of aliases possible to call the command in Discord.
			* types_options: a list or types (str, int, float...) in order of arguments in _function. Use to convert str -> type.
			* check: a function which return a boolean to ckeck if the command must be executed or not, by default, there isn't check.
		"""

		self.name = name
		self.aliases = list(aliases)
		self.types_options = types_options
		if isfunction(_function):
			self._fct = _function
			self.nb_args = len(signature(self._fct).parameters) - 1  # -1 to not take Message argument
		else:
			raise TypeError(f"_function must be a function, not a {type(_function)}")
		if check is None or isfunction(check):
			self.check = check
		else:
			raise TypeError(f"check must be a function, not a {type(check)}")

	def name_isValid(self, name: str):
		if isinstance(name, str):
			return name == self.name or name in self.aliases
		raise TypeError(f"`name` must be a str, not {type(name)}")

	async def execute(self, *args):

		if self.check is not None and self.check(message):
			try:
				new_args = [args[0]] + utils.convert_list_str(list(args[1:]), self.types_options)
			except ValueError as e:
				raise errors.DiscordTypeError(e, self)
			except TypeError as e:
				raise errors.MissingArgumentsError(e, self)

			if len(new_args) - 1 < self.nb_args:
				raise errors.MissingArgumentsError(TypeError("Missing 1 or more required positional argument"), self)

			try:
				if isroutine(self._fct):
					return await self._fct(*new_args)
				else:
					return self._fct(*new_args)

			except Exception as e:
				raise errors.CommandError(e, self)
		else:
			raise errors.ConditionError(self)


class CommandAdmin(Command):
	"""Command for admin of guild."""
	
	def __init__(self, _function, name: str = None, aliases: list = [], types_options: list = [], check=None):
		super().__init__(_function, name, aliases, types_options, check)

	async def execute(self, message, *args):
		if message.author.guild_permissions.administrator:
			await super().execute(message, *args)
		else:
			raise errors.DiscordPermissionError(self)


class CommandSuperAdmin(Command):
	"""Command for creator of bot and user in white list."""

	def __init__(self, bot, _function, name: str = None, aliases: list = [], types_options: list = [], check=None, white_list: list = []):
		super().__init__(_function, name, aliases, types_options, check)
		self.bot = bot
		self.white_list = white_list

	def add_user(self, user_id: int):
		if isinstance(user_id, int) and user_id not in self.white_list:
			self.white_list.append(user_id)
		elif not isinstance(user_id, int):
			raise ValueError(f"user_id argument must be a integer not {type(user_id)}")

	def remove_user(self, user_id: int):
		if isinstance(user_id, int) and user_id in self.white_list:
			self.white_list.remove(user_id)
		elif not isinstance(user_id, int):
			raise ValueError(f"user_id argument must be a integer not {type(user_id)}")

	async def execute(self, message, *args):
		if message.author == self.bot.appInfo.owner or message.author.id in self.white_list:
			await super().execute(message, *args)
		else:
			raise errors.DiscordPermissionError(self)
