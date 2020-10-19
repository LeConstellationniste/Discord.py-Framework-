import discord

class Bot(discord.Client):
	def __init__(self, prefix):
		super().__init__()
		self.url_pdp_bot = None
		self.prefix = prefix
		self.list_command = []
		self.list_listener = []

	async def on_ready(self):
		self.url_pdp_bot = self.user.avatar_url
		sep = 10*"-"
		print(sep)
		print("Logged in as")
		print(self.user.name)
		print(self.user.id)
		print(sep)

	async def on_message(self, message):
		if not message.author.bot and message.content.startswith(self.prefix):
			content = message.content[len(self.prefix):]
			options = message.content.split(" ")[1:]  # on ne prend qu'à partir de l'indice 1 : indice 0 = prefix+nom_command
			for command in self.list_command:
				if content.startswith(command.name):
					return await command.function(message, options)

	def add_command(self, command):
		self.list_command.append(command)


