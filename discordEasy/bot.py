import inspect
import traceback
import datetime

import discord

from .easyCommands.commandSet import CommandSet
from .easyCommands.command import Command
from . import errors
from .utils import Logs
from . import utils

class Bot(discord.Client):
	def __init__(self, prefix, token, send_errors: bool = False, print_traceback: bool = True, sep_args: str = " "):
		super().__init__()
		self.avatar_url = None  # avatar url of bot, initialized in 'on_ready' event
		self.prefix = prefix
		self.token = token
		self.appInfo = None  # AppInfo instance initialized in 'on_ready' event
		self.send_errors = send_errors  # If true, logs are send in private message to owner of bot
		self.print_traceback = print_traceback
		self.sep_args = sep_args
		self.commands = []
		self.listeners = []

	async def on_ready(self):
		self.avatar_url = self.user.avatar_url
		self.appInfo = await self.application_info()
		sep = 10*"-"
		print(sep)
		Logs.info("Logged in as")
		Logs.info(self.user.name)
		Logs.info(self.user.id)
		print(sep)

	async def on_message(self, message):
		if not message.author.bot and message.content.startswith(self.prefix):
			content = message.content[len(self.prefix):]
			name_command = content.split(self.sep_args)[0]
			options = [arg.strip() for arg in content.split(self.sep_args)[1:]]
			for command in self.commands:
				if command.check_name(name_command):
					try:
						await command.execute(message, *options)
					except errors.CommandError as e:
						try:
							await self.on_command_error(e, message)
						except Exception as e:
							await self.on_command_error(errors.CommandError(e, command), message)

	async def send_error_to_owner(self, error, traceback_msg, where):
		em = discord.Embed(title="Error raised", colour=discord.Colour.red())
		em.description = f"A error {type(error)} was raised in {where}:\n```{traceback_msg}```"
		em.timestamp = datetime.datetime.utcnow()
		await self.appInfo.owner.send(embed=em)

	async def on_command_error(self, error, message):

		if isinstance(error, errors.MissingArgumentsError):
			await self.on_missing_arguments(message.channel)
		elif isinstance(error, errors.DiscordTypeError):
			await self.on_type_error(message.channel, error.cmd.types_options)
		elif isinstance(error.origin, discord.errors.Forbidden):
			await self.on_permission_error(message)
		else:
			print()
			Logs.error(error.message)
			traceback_msg = traceback.format_exc()
			if self.send_errors:
				await self.send_error_to_owner(error, traceback_msg, error.cmd._fct.__name__)
			if self.print_traceback:
				print(traceback_msg)

	async def on_missing_arguments(self, channel):
		if not isinstance(channel, discord.TextChannel):
			raise TypeError("channel must be a discord.TextChannel")

		msg_error = "Missing options to execute this command."
		embed_error = discord.Embed(title="Option Error", description=msg_error, color=discord.Colour.red())
		await channel.send(embed=embed_error)

	async def on_type_error(self, channel, types: list):
		if not isinstance(channel, discord.TextChannel):
			raise TypeError("channel must be a discord.TextChannel")

		msg_error = "One or several options have a bad type. The type of options must be, in order: " + utils.replace_multiple(str(types), ['class', '[', ']', '>', '<']).replace("'", "`")
		embed_error = discord.Embed(title="Option Error", description=msg_error, color=discord.Colour.red())
		await channel.send(embed=embed_error)

	async def on_permission_error(self, message):
		if not isinstance(message, discord.Message):
			raise TypeError("message must be a discord.Message")

		msg_error = "Missing permission to do this command."
		em_error = discord.Embed(title="Missing permission", description=msg_error, color=discord.Colour.red())
		try:
			await message.channel.send(embed=em_error)
		except discord.errors.Forbidden:
			em_error.description = f"Missing permission to send message in {message.channel.mention}."
			await message.author.send(embed=em_error)

	def add_command(self, command, types_options: list = []):
		if isinstance(command, Command):
			self.commands.append(command)
		elif inspect.isfunction(command):
			self.commands.append(Command(command, command.__name__, types_options=types_options))
		else:
			raise TypeError(f"command must be a function or a Command, not {type(command)}")

	def add_commands(self, commands_set):
		if isinstance(commands_set, dict):
			for name, cmd in commands_set.items():
				if isinstance(cmd, tuple) or isinstance(cmd, list):
					self.add_command(Command(cmd[0], name=name, types_options=cmd[1]))
				else:
					self.add_command(Command(cmd, name=name))

		elif isinstance(commands_set, list):
			for cmd in commands_set:
				if isinstance(cmd, tuple) or isinstance(cmd, list):
					self.add_command(cmd[0], cmd[1])
				else:
					self.add_command(cmd)

		elif isinstance(commands_set, CommandSet):
			...
			raise TypeError("You can't already use a CommandSet with this method, it's in progress")

		else:
			raise TypeError(f"commands_set must be a CommandSet, a dict or a list, not {type(command)}")

	def run(self):
		super().run(self.token)


