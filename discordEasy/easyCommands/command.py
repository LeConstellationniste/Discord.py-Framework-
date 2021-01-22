from inspect import isfunction, isroutine, iscoroutine, signature

import discord

from ..errors import CommandError, MissingArgumentsError, DiscordTypeError, DiscordPermissionError
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

	async def execute(self, *args):
		try:
			new_args = [args[0]] + utils.convert_list_str(list(args[1:]), self.types_options)
		except ValueError as e:
			raise DiscordTypeError(e, self)
		except TypeError as e:
			raise MissingArgumentsError(e, self)

		if len(new_args) - 1 < self.nb_args:
			raise MissingArgumentsError(TypeError("Missing 1 or more required positional argument"), self)

		try:
			if isroutine(self._fct):
				return await self._fct(*new_args)
			else:
				return self._fct(*new_args)

		except Exception as e:
			raise CommandError(e, self)


class CommandAdmin(Command):
	"""Command for admin of guild."""
	
	def __init__(self, _function, name: str = None, aliases: list = [], types_options: list = []):
		super().__init__(_function, name, aliases, types_options)

	async def execute(self, message, *args):
		if message.author.guild_permissions.administrator:
			await super().execute(message, *args)
		else:
			raise DiscordPermissionError(self)


class CommandSuperAdmin(Command):
	"""Command for creator of bot and user in white list."""

	def __init__(self, bot, _function, name: str = None, aliases: list = [], types_options: list = [], white_list: list = []):
		super().__init__(_function, name, aliases, types_options)
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
			raise DiscordPermissionError(self)
