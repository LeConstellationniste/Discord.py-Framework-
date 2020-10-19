import baseCommandSet as commands
import bot
from configs import botConfig 

client= bot.Bot(botConfig.PREFIX, botConfig.TOKEN)

for cmd in firstListCmd
    client.add_command(cmd)


client.run()