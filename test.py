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


# listerner test

async def on_typing(channel, user, when):
	await channel.send(f"{user.mention} is writting at {when}")

async def on_member_join(member):
	print(member)
	await member.guild.channels[0].send(f"{member.mention} est arrivé !")

async def on_member_remove(member):
	print(member)
	await member.guild.channels[0].send(f"{member.mention} est parti")

async def on_reaction_add(reaction, user):
	await reaction.message.channel.send("reaction ajouté")

async def on_reaction_remove(reaction, user):
	await reaction.message.channel.send("reaction retiré")

async def on_guild_channel_update(before, after):
	print(before)
	print(after)
	await before.guild.channels[0].send(f"{before.mention} mis à jour")

async def on_invite_create(invite):
	print(invite)
	await invite.guild.channels[0].send("une invitation a été créé")

async def on_bulk_message_delete(messages):
	await messages[0].channel.send("Un message a été suprimé !")

# Bot
token = ""
bot = Bot(">", token, send_errors=True)
bot.add_command(cmd1)
bot.add_commands({'repeat': cmd2, 'addition': (cmd3, [int, int])})
bot.add_listener(on_typing)
bot.add_listeners([on_invite_create, on_bulk_message_delete, on_member_join, on_member_remove, on_reaction_add, on_reaction_remove, on_guild_channel_update])
bot.run()