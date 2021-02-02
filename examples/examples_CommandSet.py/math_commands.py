"""Commands for math."""

import asyncio
import discord
from discordEasy.objects import CommandSet, command


class Math(CommandSet):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	@command(name="Addition", aliases=("addition", "Add", "add"))
	async def addition(self, message, a: float, b: float):
		await message.channel.send(f"`{a} + {b} = {a + b}`", reference=message, mention_author=False)

	@command(name="Subtraction", aliases=("subtraction", "Sub", "sub"))
	async def subtraction(self, message, a: float, b: float):
		await message.channel.send(f"`{a} - {b} = {a - b}`", reference=message, mention_author=False)

	@command(name="Product", aliases=("product", "Prod", "prod"))
	async def product(self, message, a: float, b: float):
		await message.channel.send(f"`{a}*{b} = {a*b}`", reference=message, mention_author=False)

	@command(name="Divide", aliases=("divide", "Div", "div"))
	async def divide(self, message, a: float, b: float):
		if b == 0:
			em_error = discord.Embed(title="DivideByZero Error", color=discord.Colour.red())
			em_error.description = "You can't divide by zero!"
			await message.channel.send(embed=em_error)
		else:
			await message.channel.send(f"`{a}/{b} = {a/b}`", reference=message, mention_author=False)