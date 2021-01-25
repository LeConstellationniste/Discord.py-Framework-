# Test for development

import asyncio
import discord

from discordEasy.bot import Bot
from discordEasy.easyCommands import CommandSet, command, listener, command_super_admin

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


class MyCommandSet(CommandSet):
	def __init__(self):
		super().__init__()

	@command(name="soustraction", aliases=['sous'], types_options=[int, int])
	async def soustraction(self, message, a, b):
		await message.channel.send(f"`{a} - {b} = {a-b}`")

	@listener()
	async def on_reaction_add(self, reaction, user):
		await reaction.message.channel.send('reaction ajouté 2!')

	@command(name='admin', admin=True)
	async def admin(self, message):
		await message.channel.send("tu es admin!")

	@command_super_admin(name='superAdmin', aliases=('superA', ), white_list=[508767792124657674])
	async def super_admin(self, message):
		await message.channel.send("Tu es super admin!")

@command(name='produit', aliases=('prod', ), types_options=[int, int])
async def product(message, a, b):
	await message.channel.send(f"`{a}*{b} = {a*b}`")

def check(message):
	return True

@command(name="checkTest", aliases=['check'], checks=[check])
async def check_test(message):
	await message.channel.send("check is passed")

# Bot
token = ""
bot = Bot(">", token, send_errors=True, sep_args="$")
bot.add_command(cmd1)
bot.add_commands({'repeat': cmd2, 'addition': (cmd3, [int, int])})
bot.add_listener(on_typing)
bot.add_listeners([on_invite_create, on_bulk_message_delete, on_member_join, on_member_remove, on_reaction_add, on_reaction_remove, on_guild_channel_update])
bot.add_command_set(MyCommandSet())
bot.add_command(product)
bot.add_command(check_test)
bot.run()