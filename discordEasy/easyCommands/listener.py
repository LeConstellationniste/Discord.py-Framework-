from inspect import isroutine
import asyncio

import discord

from ..errors import DiscordEventError


class Listener:
	def __init__(self, _routine, event_name: str = None):
		if isroutine(_routine):
			self._fct = _routine
		else:
			raise TypeError(f"_routine must be a routine, not a {type(_routine)}")
		self.event_name = self._fct.__name__ if event_name is None else event_name

	async def execute(self, *args):
		try:
			return await self._fct(*args)
		except Exception as e:
			raise DiscordEventError(e, self)