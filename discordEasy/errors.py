"""A module of class errors"""

class DiscordEasyError(Exception):
	"""Base class for exceptions in this module."""

	def __init__(self, error):
		self.error = error
		self.message = self.error.__repr__()
		self._type = type(self.error)

	def __repr__(self):
		return f"{type(self)}: A error was raised: {type(self.error)}:\n{self.message}"

	def __str__(self):
		return self.__repr__()


class CommandError(DiscordEasyError):
	"""Exception raised when a error in a command is raised."""

	def __init__(self, error, command):
		super().__init__(error)
		self.cmd = command


class MissingArgumentsError(CommandError):
	"""Exception raised when a missing arguments is detected in a command."""
	def __init__(self, error, command):
		super().__init__(error, command)


class DiscordTypeError(CommandError):
	"""Exception raised when a TypeError is detected in a command."""
	def __init__(self, error, command):
		super().__init__(error, command)


class DiscordEventError(DiscordEasyError):
	"""Exception raised when a error in a listener is raised."""
	def __init__(self, error, listener):
		super().__init__(error)
		self.listener = listener
