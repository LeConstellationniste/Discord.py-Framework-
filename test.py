# Test for development

import asyncio
import discord

from discordEasy.bot import Bot
from discordEasy.objects import CommandSet, command, listener

# commands test

async def cmd1(msg: discord.Message):
	await msg.channel.send(f"Bonjour {msg.author.mention} !")


async def cmd2(msg: discord.Message, a=None):
	mon_msg = f"Tu me dis\n> {a}" if a is not None else "Tu me dis rien ?"
	await msg.channel.send(mon_msg)


async def cmd3(msg: discord.Message, a: int, b: int = 0):
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
		self.description = "Un set de commandes pour tester le bot."

	@command(name="soustraction", aliases=['sous'], description="Un commande pour soustraire 2 nombres entier a et b: `a - b`.")
	async def soustraction(self, message, a: int, b: int):
		await message.channel.send(f"`{a} - {b} = {a-b}`")

	@command(name='admin', admin=True, description="Une commande pour savoir si tu es admin ou pas.")
	async def admin(self, message):
		await message.channel.send("tu es admin!")

	@command(name='superAdmin', aliases=('superA', 'SuperAdmin', 'SuperA'), description="Une commande pour savoir si tu es super admin ou pas.", super_admin=True, white_list=[])
	async def super_admin(self, message):
		await message.channel.send("Tu es super admin!")

@command(name='produit', aliases=('prod', 'product', 'Produit', 'Product', 'Prod'), description="Un commande pour multiplier 2 nombres entier a et b: `a*b`.")
async def product(message, a: int, b: int):
	await message.channel.send(f"`{a}*{b} = {a*b}`")

def check(message):
	return True

@command(name="checkTest", aliases=['check'], checks=[check])
async def check_test(message):
	await message.channel.send("check is passed")

# Bot
token = "NzA5MDI5NDQ4NTY1MTI5MjY2.Xrf9IQ.SJdLOG8ULdGACoXuDgL3sVEBC2Y"
bot = Bot(">", token, send_errors=True, sep_args="$", colour=discord.Colour.green())
bot.add_command(cmd1, description="Une commande pour que le bot te dise bonjour!")
bot.add_commands({'repeat': cmd2, 'addition': cmd3})
bot.add_listener(on_typing)
bot.add_listeners([on_invite_create, on_bulk_message_delete, on_member_join, on_member_remove, on_guild_channel_update])
bot.add_commands(MyCommandSet())
bot.add_command(product)
bot.add_command(check_test)
bot.run()
