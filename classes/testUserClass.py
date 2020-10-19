import bot

class GuildUser(Bot):
	def __init__(self, PREFIX, token):
		super().__init__()
		self.discordName = None
		self.id = id

	async def on_message(self, message):