from inspect import isroutine, isfunction
import asyncio

import discord

from ..errors import DiscordEventError


# class Listerner
class Listener:
	def __init__(self, _routine, event_name: str = None, checks: list = []):
		if isroutine(_routine):
			self._fct = _routine
		else:
			raise ValueError(f"_routine must be a routine, not a {type(_routine)}")
		self.event_name = self._fct.__name__ if event_name is None else event_name

		for check in checks:
			if not isfunction(check):
				raise ValueError(f"checks must be a list containing functions not {type(check)}")

		self.checks = checks

	def check(self, *args):
		valid = True
		for check in self.checks:
			valid = valid and check(*args)
		return valid

	async def execute(self, *args):
		if self.check(*args):
			try:
				return await self._fct(*args)
			except Exception as e:
				raise DiscordEventError(e, self)


# Decorators for easy construction of listeners

def listener(event_name: str = None, checks: list = []):
	def decorator(_fct):
		return Listener(_fct, event_name=event_name, checks=checks)
	return decorator