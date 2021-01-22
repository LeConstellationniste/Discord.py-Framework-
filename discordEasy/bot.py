import inspect
import traceback
import datetime

import discord

from .easyCommands.commandSet import CommandSet
from .easyCommands.command import Command, CommandSuperAdmin
from .easyCommands.listener import Listener
from . import errors
from .utils import Logs
from . import utils


class BaseBot(discord.Client):
	"""A base class for Bot."""

	def __init__(self, prefix, token):
		super().__init__()
		self.prefix = prefix
		self.token = token
		self.avatar_url = None  # avatar url of bot, initialized in 'on_ready' event
		self.appInfo = None  # AppInfo instance initialized in 'on_ready' event

	async def on_ready(self):
		self.avatar_url = self.user.avatar_url
		self.appInfo = await self.application_info()

	async def on_command_error(self, error, message):

		if isinstance(error, errors.MissingArgumentsError):
			await self.on_missing_arguments(message.channel)
		elif isinstance(error, errors.DiscordTypeError):
			await self.on_type_error(message.channel, error.cmd.types_options)
		elif isinstance(error, errors.ConditionError):
			await self.on_condition_error(message.channel)
		elif isinstance(error.origin, discord.errors.Forbidden):
			await self.on_permission_error(message)
		else:
			print()
			Logs.error(error.message)
			print(traceback.format_exc())

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

	async def on_forbidden_error(self, message):
		if not isinstance(message, discord.Message):
			raise TypeError("message must be a discord.Message")

		msg_error = "Missing permission to do this command."
		em_error = discord.Embed(title="Missing permission", description=msg_error, color=discord.Colour.red())
		try:
			await message.channel.send(embed=em_error)
		except discord.errors.Forbidden:
			em_error.description = f"Missing permission to send message in {message.channel.mention}."
			await message.author.send(embed=em_error)

	async def on_permission_error(self, channel):
		if not isinstance(channel, discord.TextChannel):
			raise TypeError("channel must be a discord.TextChannel")

		msg_error = "You have not the permission to do this command."
		em_error = discord.Embed(title="Missing permission", description=msg_error, color=discord.Colour.red())
		await channel.send(embed=em_error)

	async def on_condition_error(self, channel):
		if not isinstance(channel, discord.TextChannel):
			raise TypeError("channel must be a discord.TextChannel")

		msg_error = "You don't check conditions to execute this command. For more information, use the help command."
		em_error = discord.Embed(title="Missing Conditions", description=msg_error, color=discord.Colour.red())
		await channel.send(embed=em_error)


class Bot(BaseBot):
	"""Class Bot to build easier and quickly Discord bot."""

	def __init__(self, prefix, token, send_errors: bool = False, print_traceback: bool = True, sep_args: str = " "):
		super().__init__(prefix, token)
		self.send_errors = send_errors  # If true, logs are send in private message to owner of bot
		self.print_traceback = print_traceback
		self.sep_args = sep_args
		self.commands = []
		self.listeners = []

	async def check_execute_listener(self, event_name: str, *args, **kwargs):
		for listener in self.listeners:
			if listener.event_name == event_name:
				await listener.execute(*args, **kwargs)

	async def on_ready(self):  # ok
		await super().on_ready()
		sep = 10*"-"
		print(sep)
		Logs.info("Logged in as")
		Logs.info(self.user.name)
		Logs.info(self.user.id)
		print(sep)
		await self.check_execute_listener('on_ready')

	async def on_shard_ready(self, shard_id):  # ok
		await self.check_execute_listener('on_shard_ready', shard_id)

	async def on_connect(self):  # ok
		await self.check_execute_listener('on_connect')

	async def on_shard_connect(self, shard_id):  # ok
		await self.check_execute_listener('on_shard_connect', shard_id)

	async def on_disconnect(self):  # ok
		await self.check_execute_listener('on_disconnect')

	async def on_shard_disconnect(self, shard_id):  # ok
		await self.check_execute_listener('on_shard_disconnect', shard_id)

	async def on_resumed(self):
		await self.check_execute_listener('on_resumed')

	async def on_shard_resumed(self, shard_id):
		await self.check_execute_listener('on_shard_resumed', shard_id)

	async def on_typing(self, channel, user, when):  # fonctionne pas
		await self.check_execute_listener('on_typing', channel, user, when)

	async def on_message(self, message):  # ok
		if not message.author.bot and message.content.startswith(self.prefix):
			content = message.content[len(self.prefix):]
			name_command = content.split(self.sep_args)[0]
			options = [arg.strip() for arg in content.split(self.sep_args)[1:]]
			for command in self.commands:
				if command.name_isValid(name_command):
					try:
						await command.execute(message, *options)
					except errors.CommandError as e:
						try:
							await self.on_command_error(e, message)
						except Exception as e:
							await self.on_command_error(errors.CommandError(e, command), message)

		else:
			await self.check_execute_listener('on_message', message)

	async def on_message_delete(self, message):  # ok
		await self.check_execute_listener('on_message_delete', message)

	async def on_bulk_message_delete(self, messages):  # ne fonctionne pas
		await self.check_execute_listener('on_bulk_message_delete', messages)

	async def on_raw_message_delete(self, payload):  # ok
		await self.check_execute_listener('on_raw_message_delete', payload)

	async def on_raw_bulk_message_delete(self, payload):  # ne fonctionne pas
		await self.check_execute_listener('on_raw_bulk_message_delete', payload)

	async def on_message_edit(self, before, after):  # ok
		await self.check_execute_listener('on_message_edit', before, after)

	async def on_raw_message_edit(self, payload):  # ok
		await self.check_execute_listener('on_raw_message_edit', payload)

	async def on_reaction_add(self, reaction, user):  # ok
		await self.check_execute_listener('on_reaction_add', reaction, user)

	async def on_raw_reaction_add(self, payload):  # ok
		await self.check_execute_listener('on_raw_reaction_add', payload)

	async def on_reaction_remove(self, reaction, user):  # fonctionne pas
		await self.check_execute_listener('on_reaction_remove', reaction, user)

	async def on_raw_reaction_remove(self, payload):  # fonctionne pas
		await self.check_execute_listener('on_raw_reaction_remove', payload)

	async def on_reaction_clear(self, message, reaction):
		await self.check_execute_listener('on_reaction_clear', message, reaction)

	async def on_raw_reaction_clear(self, payload):
		await self.check_execute_listener('on_raw_reaction_clear', payload)

	async def on_reaction_clear_emoji(self, reaction):
		await self.check_execute_listener('on_reaction_clear_emoji', reaction)

	async def on_raw_reaction_clear_emoji(self, payload):
		await self.check_execute_listener('on_raw_reaction_clear_emoji', payload)

	async def on_private_channel_delete(self, channel):
		await self.check_execute_listener('on_private_channel_delete', channel)

	async def on_private_channel_create(self, channel):
		await self.check_execute_listener('on_private_channel_create', channel)

	async def on_private_channel_update(self, before, after):
		await self.check_execute_listener('on_private_channel_update', before, after)

	async def on_guild_channel_delete(self, channel):
		await self.check_execute_listener('on_guild_channel_delete', channel)

	async def on_guild_channel_create(self, channel):
		await self.check_execute_listener('on_guild_channel_create', channel)

	async def on_guild_channel_update(self, before, after):
		await self.check_execute_listener('on_guild_channel_update', before, after)

	async def on_guild_channel_pins_update(self, channel, last_pin):
		await self.check_execute_listener('on_guild_channel_pins_update', channel, last_pin)

	async def on_guild_integrations_update(self, guild):
		await self.check_execute_listener('on_guild_integrations_update', guild)

	async def on_webhooks_update(self, channel):
		await self.check_execute_listener('on_webhooks_update', channel)

	async def on_member_join(self, member):  # fonctionne pas
		await self.check_execute_listener('on_member_join', member)

	async def on_member_remove(self, member):  # fonctionne pas
		await self.check_execute_listener('on_member_remove', member)

	async def on_member_update(self, before, after):  # fonctionne pas
		await self.check_execute_listener('on_member_update', before, after)

	async def on_user_update(self, before, after):
		await self.check_execute_listener('on_user_update', before, after)

	async def on_guild_join(self, guild):
		await self.check_execute_listener('on_guild_join', guild)

	async def on_guild_remove(self, guild):
		await self.check_execute_listener('on_guild_remove', guild)

	async def on_guild_update(self, before, after):
		await self.check_execute_listener('on_guild_update', before, after)

	async def on_guild_role_update(self, before, after):
		await self.check_execute_listener('on_guild_role_update', before, after)

	async def on_guild_emojis_update(self, guild, before, after):
		await self.check_execute_listener('on_guild_emojis_update', guild, before, after)

	async def on_guild_available(self, guild):
		await self.check_execute_listener('on_guild_available', guild)

	async def on_voice_state_update(self, member, before, after):
		await self.check_execute_listener('on_voice_state_update', member, before, after)

	async def on_member_ban(self, guild, user):
		await self.check_execute_listener('on_member_ban', guild, user)

	async def on_member_unban(self, guild, user):
		await self.check_execute_listener('on_member_unban', guild, user)

	async def on_invite_create(self, invite):
		await self.check_execute_listener('on_invite_create', invite)

	async def on_invite_delete(self, invite):
		await self.check_execute_listener('on_invite_delete', invite)

	async def on_group_join(self, channel, user):
		await self.check_execute_listener('on_group_join', channel, user)

	async def on_group_remove(self, channel, user):
		await self.check_execute_listener('on_group_remove', channel, user)

	async def on_relationship_add(self, relationship):
		await self.check_execute_listener('on_relationship_add', relationship)

	async def on_relationship_remove(self, relationship):
		await self.check_execute_listener('on_relationship_remove', relationship)

	async def on_relationship_update(self, before, after):
		await self.check_execute_listener('on_relationship_update', before, after)

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

		elif isinstance(error, errors.DiscordPermissionError):
			await self.on_permission_error(message.channel)

		elif isinstance(error, errors.ConditionError):
			await self.on_condition_error(message.channel)

		elif isinstance(error.origin, discord.errors.Forbidden):
			await self.on_forbidden_error(message)

		else:
			print()
			Logs.error(error.message)
			traceback_msg = traceback.format_exc()
			if self.send_errors:
				await self.send_error_to_owner(error, traceback_msg, error.cmd._fct.__name__)
			if self.print_traceback:
				print(traceback_msg)

	def add_command(self, command, check=None, types_options: list = [], super_admin: bool = False, white_list: list = []):
		if isinstance(command, Command):
			self.commands.append(command)
		elif inspect.isfunction(command) and not super_admin:
			self.commands.append(Command(command, command.__name__, types_options=types_options, check=check))
		elif inspect.isfunction(command):
			self.commands.append(CommandSuperAdmin(self, command, command.__name__, types_options=types_options, check=check, white_list=white_list))
		else:
			raise ValueError(f"command must be a function or a Command, not {type(command)}")

	def add_listener(self, listener, event_name: str = None):
		if isinstance(listener, Listener):
			self.listeners.append(listener)
		elif inspect.isroutine(listener):
			self.listeners.append(Listener(listener, event_name))
		else:
			raise ValueError(f"listener must be a Listener or a routine, not {type(listener)}")

	def add_commands(self, commands_set, check=None, super_admin: bool = False, white_list: list = []):
		if isinstance(commands_set, dict):
			for name, cmd in commands_set.items():
				if (isinstance(cmd, tuple) or isinstance(cmd, list)) and not super_admin:
					self.add_command(Command(cmd[0], check=check, name=name, types_options=cmd[1]))
				elif isinstance(cmd, tuple) or isinstance(cmd, list):
					self.add_command(CommandSuperAdmin(self, cmd[0], check=check, name=name, types_options=cmd[1]))
				elif super_admin:
					self.add_command(CommandSuperAdmin(self, cmd, check=check, name=name))
				else:
					self.add_command(Command(cmd, check=check, name=name))

		elif isinstance(commands_set, list):
			for cmd in commands_set:
				if isinstance(cmd, tuple) or isinstance(cmd, list):
					self.add_command(cmd[0], check=check, types_options=cmd[1], super_admin=super_admin, white_list=white_list)
				else:
					self.add_command(cmd, check=check, super_admin=super_admin, white_list=white_list)

		elif isinstance(commands_set, CommandSet):
			...
			raise ValueError("You can't already use a CommandSet with this method, it's in progress")

		else:
			raise ValueError(f"commands_set must be a CommandSet, a dict or a list, not {type(command)}")

	def add_listeners(self, listeners):
		if isinstance(listeners, dict):
			for event_name, listener in listeners.items():
				self.add_listener(listener, event_name=event_name)
		elif isinstance(listeners, list) or isinstance(listeners, tuple):
			for listener in listeners:
				self.add_listener(listener)

	def run(self):
		super().run(self.token)


