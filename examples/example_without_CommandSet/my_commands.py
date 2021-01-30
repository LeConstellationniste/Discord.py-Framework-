import asyncio
import discord

# Just function to add to the bot
async def hello(message):
	await message.channel.send(f"Hello {message.author.mention}!", reference=message.to_reference())


async def admin(message):
	await message.channel.send(f"Hello {message.author.mention}! You are administrator!", reference=message.to_reference())

async def product(message, a, b):
	await message.channel.send(f"`{a}*{b} = {a*b}`", reference=message.to_reference())


# Or Command create with this function
from discordEasy.objects import Command, CommandAdmin

async def hello(message):
	await message.channel.send(f"Hello {message.author.mention}!", reference=message.to_reference())


async def admin(message):
	await message.channel.send(f"Hello {message.author.mention}! You are administrator!", reference=message.to_reference())

async def product(message, a, b):
	await message.channel.send(f"`{a}*{b} = {a*b}`", reference=message.to_reference())

cmd_hello = Command(hello, name="Hello", aliases=("hello", "Hi", "hi"))
cmd_admin = CommandAdmin(admin, name="Admin")
cmd_product = Command(product, name="Product", types_options=[int, int])