from inspect import iscoroutinefunction
import asyncio

import discord

from ..errors import DiscordEventError


class Listener:
	def __init__(self, _coroutine, event_name: str = None):
		if iscoroutinefunction(_coroutine):
			self._fct = _coroutine
		else:
			raise TypeError(f"_coroutine must be a coroutine function, not a {type(_coroutine)}")
		self.event_name = self._fct.__name__ if event_name is None else event_name

	async def execute(self, *args):
		try:
			return self._fct(*args)
		except Exception as e:
			raise DiscordEventError(e, self)