"""Commands for math."""

import asyncio
import discord
from discordEasy.objects import CommandSet, command


class Math(CommandSet):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	@command(name="Addition", aliases=("addition", "Add", "add"), types_options=[float, float])
	async def addition(self, message, a, b):
		await message.channel.send(f"`{a} + {b} = {a + b}`", reference=message, mention_author=False)

	@command(name="Subtraction", aliases=("subtraction", "Sub", "sub"), types_options=[float, float])
	async def subtraction(self, message, a, b):
		await message.channel.send(f"`{a} - {b} = {a - b}`", reference=message, mention_author=False)

	@command(name="Product", aliases=("product", "Prod", "prod"), types_options=[float, float])
	async def product(self, message, a, b):
		await message.channel.send(f"`{a}*{b} = {a*b}`", reference=message, mention_author=False)

	@command(name="Divide", aliases=("divide", "Div", "div"), types_options=[float, float])
	async def divide(self, message, a, b):
		if b == 0:
			em_error = discord.Embed(title="DivideByZero Error", color=discord.Colour.red())
			em_error.description = "You can't divide by zero!"
			await message.channel.send(embed=em_error)
		else:
			await message.channel.send(f"`{a}/{b} = {a/b}`", reference=message, mention_author=False)