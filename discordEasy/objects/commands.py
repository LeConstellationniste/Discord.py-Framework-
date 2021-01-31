from inspect import isfunction, ismethod, isroutine, iscoroutine, signature

import discord

from .. import errors
from .. import utils


# Class Command
class Command:
	def __init__(self, _function, name: str = None, aliases: list = [], types_options: list = [], checks: list = []):
		""" Arguments:
			* _function: the function to execute, it's the base of command
			* name: the name of command, if None, the name attribute of function is used. It's the name which is used in Discord to call the command.
			* aliases: a list of aliases possible to call the command in Discord.
			* types_options: a list or types (str, int, float...) in order of arguments in _function. Use to convert str -> type.
			* check: a function which return a boolean to ckeck if the command must be executed or not, by default, there isn't check.
		"""

		self.name = name
		if isinstance(aliases, list) or isinstance(aliases, tuple):
			self.aliases = list(aliases)
		else:
			raise ValueError(f"aliases must be a list or tuple, not a {type(aliases)}")
		self.types_options = types_options
		if isfunction(_function):
			self._fct = _function
			self.nb_args = len(signature(self._fct).parameters) - 1  # -1 to not take Message argument
		else:
			raise ValueError(f"_function must be a function, not a {type(_function)}")
		
		for check in checks:
			if not isfunction(check):
				raise ValueError(f"checks must be a list containing functions not {type(check)}")

		self.checks = checks

	def name_isValid(self, name: str):
		if isinstance(name, str):
			return name == self.name or name in self.aliases
		raise ValueError(f"`name` must be a str, not {type(name)}")

	def check(self, message):
		valid = True
		for check in self.checks:
			valid = valid and check(message)
		return valid

	async def execute(self, message, *args, cmd_set_instance=None):
		if self.check(message):
			try:
				base_args = [message] if cmd_set_instance is None else [cmd_set_instance, message]
				new_args = base_args + utils.convert_list_str(list(args), self.types_options)
			except ValueError as e:
				raise errors.DiscordTypeError(e, self)
			except TypeError as e:
				raise errors.MissingArgumentsError(e, self)

			if len(args) < self.nb_args:
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
	
	def __init__(self, _function, name: str = None, aliases: list = [], types_options: list = [], checks: list = []):
		super().__init__(_function, name, aliases, types_options, checks)

	async def execute(self, message, *args, cmd_set_instance=None):
		if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel) or message.author.guild_permissions.administrator:
			await super().execute(message, *args, cmd_set_instance=cmd_set_instance)
		else:
			raise errors.DiscordPermissionError(self)


class CommandSuperAdmin(CommandAdmin):
	"""Command for creator of bot and user in white list. User must be also a administrator."""

	def __init__(self, _function, name: str = None, aliases: list = [], types_options: list = [], checks: list = [], white_list: list = []):
		super().__init__(_function, name, aliases, types_options, checks)
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

	async def execute(self, message, *args, cmd_set_instance=None):
		if message.author.id in self.white_list:
			await super().execute(message, *args, cmd_set_instance=cmd_set_instance)
		else:
			raise errors.DiscordPermissionError(self)


# Decorator for easy construction of command

def command(name: str = None, aliases: list = [], types_options: list = [], checks: list = [], admin: bool = False, super_admin: bool = False, white_list: list = []):
	def decorator(_fct):
		if super_admin:
			return CommandSuperAdmin(_fct, name=name, aliases=aliases, types_options=types_options, checks=checks, white_list=white_list)
		elif admin:
			return CommandAdmin(_fct, name=name, aliases=aliases, types_options=types_options, checks=checks)
		return Command(_fct, name=name, aliases=aliases, types_options=types_options, checks=checks)
	return decorator
