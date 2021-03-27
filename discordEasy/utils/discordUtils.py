# Function to facilitate certain tasks on Discord
import discord
import asyncio

from .logs import Logs


async def safe_delete(message: discord.Message, delay_: int = 0, warning: bool = True) -> None:
	if isinstance(message, discord.Message):
		try:
			await message.delete(delay=delay_)
		except discord.Forbidden:
			Logs.warning("Delete message failed: the bot had not the permission 'manage_guild' or the message is a DM.")
		except discord.NotFound:
			pass