import command

async def function1(message, option1):
	await message.channel.send(f"Tu me dit : {option1}")

command1 = command.Command(function1, name="command1", aliases=("C1", ))