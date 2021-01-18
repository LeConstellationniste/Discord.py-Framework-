# Test for development

import asyncio
import discord

from discordEasy.bot import Bot

# commands test

async def cmd1(msg: discord.Message):
	await msg.channel.send(f"Bonjour {msg.author.mention} !")


async def cmd2(msg: discord.Message, a):
	await msg.channel.send(f"Tu me dis {a}")


# Bot
token = "token"
bot = Bot(">", token)
bot.add_command(cmd1)
bot.add_command(cmd2)
bot.run()