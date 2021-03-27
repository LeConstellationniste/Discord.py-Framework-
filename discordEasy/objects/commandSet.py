from typing import Union, Iterable, Coroutine

from inspect import getmembers
import asyncio

import discord

from . import Listener, listener, Command, command, CommandAdmin, CommandSuperAdmin
from ..utils import list_to_str, Logs


class CommandSet:
	"""Base class to create a group of commands and listeners"""

	def __init__(self, name: str = None):
		methods = getmembers(self)
		self.commands = {method[1].name: method[1] for method in methods if isinstance(method[1], Command)}
		self.listeners = {method[1].event_name: method[1] for method in methods if isinstance(method[1], Listener)}
		self.name = name if name is not None  else type(self).__name__
		self.description = ""

	async def execute_cmd(self, message: discord.Message, name: str, options: Iterable) -> None:
		for cmd in self.commands.values():
			if cmd.name_isValid(name):
				await cmd.execute(message, cmd_set_instance=self, *options)

	async def execute_listener(self, event_name: str, *args, **kwargs) -> None:
		for listener in self.listeners.values():
			if listener.event_name == event_name:
				await listener.execute(self, *args, **kwargs)


class BaseHelp(CommandSet):
	"""A base class for help command, this class is used also for the default help command."""

	def __init__(self, bot):
		super().__init__()
		self.description = "The help commands to learn how to use the bot."
		self.bot = bot
		self.name = "Commands Help"

	def base_embed(self, title: str, description: str = "", author: discord.Member = None) -> discord.Embed:
		em = discord.Embed(title=title, description=description, color=self.bot.colour)
		if author is not None:
			em.set_author(name=author.name, icon_url=author.avatar_url)
		em.set_thumbnail(url=self.bot.avatar_url)
		return em

	def first_page(self, author: discord.Member = None) -> discord.Embed:
		desc_bot = f"""{self.bot.description}\n\nPrefix: `{self.bot.prefix}`\nAuthor: {self.bot.app_info.owner.name}"""
		em = self.base_embed(f"Help {self.bot.app_info.name}", description=desc_bot, author=author)
		msg_help = f"""To get this message use the command `help`: `{self.bot.prefix}help`.
		Aliases: {list_to_str(self.commands['help'].aliases).replace("'", "`")}"""
		em.add_field(name="Help command", value=msg_help)
		return em

	def command_pages(self, set_commands: Union[CommandSet, Iterable], author: discord.Member) -> list:
		title = f"Help {set_commands.name}" if isinstance(set_commands, CommandSet) else f"Help {self.bot.app_info.name}"
		description = set_commands.description if isinstance(set_commands, CommandSet) else ""
		em = self.base_embed(title, description, author=author)
		pages = [em]
		list_commands = set_commands.commands.values() if isinstance(set_commands, CommandSet) else set_commands
		nb_pages = 1
		nb_cmd = 0
		for cmd in list_commands:
			if nb_cmd == 8:
				em = self.base_embed(title=title, description=description, author=author)
				pages.append(em)
				nb_cmd = 0
				nb_pages += 1
			if (type(cmd) == CommandAdmin and isinstance(author, discord.Member) and author.guild_permissions.administrator) or (type(cmd) == CommandSuperAdmin and author.id in cmd.white_list) or type(cmd) == Command:
				msg = f"""{cmd.description}\nName: `{cmd.name}`\nAliases: {list_to_str(cmd.aliases).replace("'", "`")}"""
				em.add_field(name=f"Command {cmd.name}", value=msg, inline=False)
				nb_cmd += 1
		return [em for em in pages if len(em.fields) > 0]


	@command(name="help", aliases=("Help", ), delete_message=True, description="The general help command.")
	async def help(self, msg):
		def check(reaction, user):
			return not user.bot and str(reaction.emoji) in ("◀️", "▶️", "⏹️")

		pages = [self.first_page(msg.author)] + self.command_pages(self.bot.commands, msg.author)
		for cmd_set in self.bot.list_set:
			pages += self.command_pages(cmd_set, msg.author)
		nb_pages = len(pages)
		current_page = 1

		current_embed = pages[current_page-1]
		current_embed.set_footer(text=f"page: {current_page}/{nb_pages}")
		help_msg = await msg.channel.send(embed=current_embed)
		await help_msg.add_reaction("◀️")
		await help_msg.add_reaction("⏹️")
		await help_msg.add_reaction("▶️")

		while help_msg is not None:
			try:
				reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
				# waiting for a reaction to be added. Times out after 60 seconds
				if str(reaction.emoji) == "▶️" and current_page != nb_pages:
					current_page += 1
					current_embed = pages[current_page - 1]
					current_embed.set_footer(text=f"page: {current_page}/{nb_pages}")
					await help_msg.edit(embed=current_embed)

				elif str(reaction.emoji) == "▶️":
					current_page = 1
					current_embed = pages[current_page - 1]
					current_embed.set_footer(text=f"page: {current_page}/{nb_pages}")
					await help_msg.edit(embed=current_embed)

				elif str(reaction.emoji) == "◀️" and current_page > 1:
					current_page -= 1
					current_embed = pages[current_page - 1]
					current_embed.set_footer(text=f"page: {current_page}/{nb_pages}")
					await help_msg.edit(embed=current_embed)

				elif str(reaction.emoji) == "◀️":
					current_page = nb_pages
					current_embed = pages[current_page - 1]
					current_embed.set_footer(text=f"page: {current_page}/{nb_pages}")
					await help_msg.edit(embed=current_embed)

				elif str(reaction.emoji) == "⏹️":
					await help_msg.delete(delay=1)
					break

				try:
					await help_msg.remove_reaction(reaction, user)
				except discord.errors.Forbidden:
					pass

			except asyncio.TimeoutError:
				try:
					await help_msg.remove_reaction("◀️", self.bot.user)
					await help_msg.remove_reaction("⏹️", self.bot.user)
					await help_msg.remove_reaction("▶️", self.bot.user)
					break
				except discord.errors.Forbidden:
					pass

			except discord.errors.Forbidden:
				pass

	@staticmethod
	def setup(bot):
		bot.add_commands(BaseHelp(bot))


class DevCommands(CommandSet):
	"""A base class for development commands."""

	def __init__(self, bot):
		super().__init__()
		self.description = "The utils commands to development."
		self.bot = bot
		self.name = "Development Commands"

	@command(name="stopBot", aliases=("StopBot", "StopB", "stopB"), delete_message=True, super_admin=True, description="Disconnect the bot")
	async def stop(self, msg):
		em = discord.Embed(title="Logout in progress...", color=self.bot.colour)
		em.description = "The bot will be logout in 5 seconds."
		await msg.channel.send(embed=em, delete_after=4)
		Logs.warning(f"{msg.author.name} disconnected the bot.")
		await asyncio.sleep(5)
		await self.bot.logout()

	@listener()
	async def on_ready(self):
		self.commands["stopBot"].add_user(self.bot.app_info.owner.id)

	@staticmethod
	def setup(bot):
		bot.add_commands(DevCommands(bot))


