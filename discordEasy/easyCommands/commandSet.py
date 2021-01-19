import discord


class CommandSet:
	"""Class to create a group of commands and listeners"""

	def __init__(self, bot):
		self.bot = bot

	@classmethod
	def setup(cls, bot, *args, **kwargs):
		bot.add_commands(cls(bot, *args, **kwargs))
