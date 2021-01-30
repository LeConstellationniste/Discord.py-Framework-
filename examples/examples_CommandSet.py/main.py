"""
Example with OOP.

This script is the main Python script of your bot, here, the bot is initialized.
"""

from discordEasy import Bot

from help import Help
from math_commands import Math


my_token_bot = ""
my_prefix_bot = ">"

# The arguments 'print_traceback', 'send_errors' and 'sep_args' have by default the same values as below, they have been explained just for the example.
my_bot = Bot(prefix=my_prefix_bot, token=my_token_bot, print_traceback=True, send_errors=False, sep_args= " ")

my_bot.add_commands(Help(my_bot))
my_bot.add_commands(Math(my_bot))

my_bot.run()