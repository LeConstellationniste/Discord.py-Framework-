"""A module of class errors"""

class Error(Exception):
	"""Base class for exceptions in this module."""

	def __init__(self, message: str = ""):
		self.message = message


class ArgumentsError(Error):
	def __init__(self, message):
		Error.__init__(self, message)
