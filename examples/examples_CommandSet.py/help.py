"""A help class to define help commands."""

import asyncio
import discord
from discordEasy.objects import CommandSet, command


class Help(CommandSet):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	@command(name='Help', aliases=("help", "H", "h"))
	async def help(self, message):
		help_embed = discord.Embed(title="Help", color=discord.Colour.blue())
		help_embed.description = f"""{self.bot.app_info.name} is a test bot.\n\nPrefix of the bot: `"{self.bot.prefix}"`\n\nIf a command requires options, you must separate the options by: `"{self.bot.sep_args}"`.\n\n"""
		help_math = f"""Commands Math:
		* `Addition`: Addition of 2 numbers `a` & `b`. Example: `{self.bot.prefix}Addition 1{self.bot.sep_args}1`. Aliases: `addition`, `Add`, `add`.
		* `Subtraction`: Subtraction of 2 numbers `a` & `b`. Example: `{self.bot.prefix}Subtraction 1{self.bot.sep_args}1`. Aliases: `substraction`, `Sub`, `sub`.
		* `Product`: Product of 2 numbers `a` & `b`. Example: `{self.bot.prefix}Product 1{self.bot.sep_args}1`. Aliases: `product`, `Prod`, `prod`.
		* `Divide`: Divide of 2 numbers `a` & `b`. Example: `{self.bot.prefix}Divide 1{self.bot.sep_args}1`. Aliases: `divide`, `Div`, `div`."""
		help_embed.description += help_math
		help_embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
		await message.channel.send(embed=help_embed)