
import discord

class Command:
	def __init__(self, fct, name=None, checks, aliases: tuple = None):
		self.function = fct
		self.name = fct.__name__ if name is None else name
		self.aliases = aliases
		self.checks = checks
