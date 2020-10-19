import baseCommandSet as commands
import bot
from configs import botConfig 

client= bot.Bot(botConfig.PREFIX, botConfig.TOKEN)

client.add_command(commands.command1)

client.run()