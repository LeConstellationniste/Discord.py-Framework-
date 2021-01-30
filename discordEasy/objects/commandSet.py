from inspect import getmembers

import discord

from . import Listener, Command


class CommandSet:
	"""Base class to create a group of commands and listeners"""

	def __init__(self):
		methods = getmembers(self)
		self.commands = [method for name, method in methods if isinstance(method, Command)]
		self.listeners = [method for name, method in methods if isinstance(method, Listener)]
		for cmd in self.commands:
			cmd.nb_args -= 1  # -1 to don't take the __self__ argument

	async def execute_cmd(self, message, name, options):
		for cmd in self.commands:
			if cmd.name_isValid(name):
				await cmd.execute(message, cmd_set_instance=self, *options)

	async def execute_listener(self, event_name, *args, **kwargs):
		for listener in self.listeners:
			if listener.event_name == event_name:
				await listener.execute(self, *args, **kwargs)

