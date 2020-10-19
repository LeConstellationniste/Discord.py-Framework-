import discord

class Bot(discord.Client):
	def __init__(self, prefix, token):
		super().__init__()
		self.url_pdp_bot = None
		self.prefix = prefix
		self.token = token
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
			cmd = content.split(" ")[0]
			args = content.split(" ")[1:]
			for command in self.list_command:
				if cmd == command.name or cmd in command.aliases:
					try:
						await command.function(message, *args)
					except TypeError:
						await self.argument_error(message.channel)

	async def argument_error(self, channel):
		if not isinstance(channel, discord.TextChannel):
			raise TypeError("channel must be a discord.TextChannel")
		else:
			msg_error = "Missing args to execute this command."
			embed_error = discord.Embed(title="Option Error", description=msg_error, color=discord.Colour.red())
			await channel.send(embed=embed_error)

	def add_command(self, command):
		self.list_command.append(command)

	def add_listener(self, listener):
		...  # Il faut créer la classe Listener

	def run(self):
		super().run(self.token)


