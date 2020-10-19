
import discord

class Command:
	def __init__(self, name, fct, checks:list, aliases: tuple = None):
		self.name = fct
		self.functionLoc = fct
		self.checksLoc = checks
		self.aliases = aliases
	async def awaitOfFunc(self, args,author,chan,guild):
		if check...
			way = self.functionLoc
			way(args,author,chan,guild)