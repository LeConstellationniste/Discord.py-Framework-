# Test for development

import asyncio
import discord

from discordEasy.bot import Bot

# commands test

async def cmd1(msg: discord.Message):
	await msg.channel.send(f"Bonjour {msg.author.mention} !")


async def cmd2(msg: discord.Message, a):
	await msg.channel.send(f"Tu me dis\n> {a}")


async def cmd3(msg: discord.Message, a, b):
	await msg.channel.send(f"Le résultat est : `{a} + {b} = {int(a)+int(b)}`")

# Bot
token = "token"
bot = Bot(">", token, send_errors=True)
bot.add_command(cmd1)
bot.add_commands({'repeat': cmd2, 'addition': (cmd3, [int, int])})
bot.run()