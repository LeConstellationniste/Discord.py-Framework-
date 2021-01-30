import asyncio
import discord


# Just with a function to add to the bot.
async def on_message(message):
	if not message.author.bot:
		await message.channel.send(f"{message.author.mention} a envoyé un message!")

# A Listener already created with the function
from discordEasy.objects import Listener

async def on_message(message):
	if not message.author.bot:
		await message.channel.send(f"{message.author.mention} a envoyé un message!")

listener_on_message = Listener(on_message)