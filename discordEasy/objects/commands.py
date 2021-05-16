from typing import Union, Iterable, Coroutine, Callable

from inspect import isfunction, ismethod, isroutine, iscoroutine, signature, _empty

import discord

from .. import errors
from .. import utils


# Class Command
class Command:
	def __init__(self, _function: Union[Callable, Coroutine], name: str = None, aliases: Iterable[str] = [], checks: Iterable[Callable] = [],
				delete_message: bool = False, description: str = "", example: Iterable[str] = None):
		""" Arguments:
			* _function: the function to execute, it's the base of command
			* name: the name of command, if None, the name attribute of function is used. It's the name which is used in Discord to call the command.
			* aliases: a list of aliases possible to call the command in Discord.
			* check: a function which return a boolean to ckeck if the command must be executed or not, by default, there isn't check.
			* description: a short description (str) for the command.
		"""

		self.name = name
		if isinstance(aliases, list) or isinstance(aliases, tuple):
			self.aliases = list(aliases)
		else:
			raise ValueError(f"aliases must be a list or tuple, not a {type(aliases)}")
		if isfunction(_function):
			self._fct = _function
			self.args_signature = [{"name": k,
									"type": v.annotation if isinstance(v.annotation, type) else _empty, 
									"default": v.default} for k, v in signature(self._fct).parameters.items() if k != 'self'][1:]  # delete first item which is the Message object.
		else:
			raise ValueError(f"_function must be a function, not a {type(_function)}")
		
		for check in checks:
			if not isfunction(check):
				raise ValueError(f"checks must be a list containing functions not {type(check)}")

		self.checks = checks
		self.delete_message = delete_message
		self.description = description
		self.example = example

	def name_isValid(self, name: str) -> bool:
		if isinstance(name, str):
			return name == self.name or name in self.aliases
		raise ValueError(f"`name` must be a str, not {type(name)}")

	def check(self, message: discord.Message) -> bool:
		valid = True
		for check in self.checks:
			valid &= check(message)
		return valid

	async def execute(self, message: discord.Message, *args, cmd_set_instance=None, **kwargs):
		if self.delete_message:
			await utils.safe_delete(message, delay_=3)
		if self.check(message):
			try:
				new_args = [message] if cmd_set_instance is None else [cmd_set_instance, message]
				n_base_args = len(new_args)
				new_args += args[:len(self.args_signature)]

				for i in range(len(new_args) - n_base_args, len(self.args_signature)):
					if self.args_signature[i]['default'] is not _empty:
						new_args.append(self.args_signature[i]['default'])
					else:
						raise TypeError("Missing 1 required positional argument")

				for i, arg in enumerate(new_args[n_base_args:]):
					if self.args_signature[i]['type'] != _empty:
						new_args[i+n_base_args] = self.args_signature[i]['type'](arg)


			except ValueError as e:
				raise errors.DiscordTypeError(e, self)

			except TypeError as e:
				raise errors.MissingArgumentsError(e, self)

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
	
	def __init__(self, _function: Union[Callable, Coroutine], **kwargs):
		super().__init__(_function, **kwargs)

	async def execute(self, message: discord.Message, *args, cmd_set_instance=None) -> None:
		if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel) or message.author.guild_permissions.administrator:
			await super().execute(message, *args, cmd_set_instance=cmd_set_instance)
		else:
			raise errors.DiscordPermissionError(self)


class CommandSuperAdmin(CommandAdmin):
	"""Command for creator of bot and user in white list. User must be also a administrator."""

	def __init__(self, _function: Union[Callable, Coroutine], white_list: Iterable[int] = [], **kwargs):
		super().__init__(_function, **kwargs)
		self.white_list = white_list

	def add_user(self, user_id: int) -> None:
		if isinstance(user_id, int) and user_id not in self.white_list:
			self.white_list.append(user_id)
		elif not isinstance(user_id, int):
			raise ValueError(f"user_id argument must be a integer not {type(user_id)}")

	def remove_user(self, user_id: int) -> None:
		if isinstance(user_id, int) and user_id in self.white_list:
			self.white_list.remove(user_id)
		elif not isinstance(user_id, int):
			raise ValueError(f"user_id argument must be a integer not {type(user_id)}")

	async def execute(self, message: discord.Message, *args, cmd_set_instance=None) -> None:
		if message.author.id in self.white_list:
			await super().execute(message, *args, cmd_set_instance=cmd_set_instance)
		else:
			raise errors.DiscordPermissionError(self)


# Decorator for easy construction of command

def command(name: str = None, aliases: Iterable[str] = [], checks: Iterable[Callable] = [], delete_message: bool = False,
			description: str = "", example: Iterable[str] = None, admin: bool = False, super_admin: bool = False, white_list: Iterable[int] = []):
	def decorator(_fct):
		if super_admin:
			return CommandSuperAdmin(_fct, name=name, aliases=aliases, checks=checks, delete_message=delete_message,
						description=description, example=example, white_list=white_list)
		elif admin:
			return CommandAdmin(_fct, name=name, aliases=aliases, checks=checks, delete_message=delete_message,
						description=description, example=example)
		return Command(_fct, name=name, aliases=aliases, checks=checks, delete_message=delete_message,
					description=description, example=example)
	return decorator
