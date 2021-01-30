"""
Example without OOP.
"""

from discordEasy import bot

from my_commands import *
from my_listeners import *


my_token_bot = "YourToken"
my_prefix_bot = ">"


# The arguments 'print_traceback', 'send_errors' and 'sep_args' have by default the same values as below, they have been explained just for the example.
my_bot = Bot(prefix=my_prefix_bot, token=my_token_bot, print_traceback=True, send_errors=False, sep_args= " ")

# Just functions was created
my_bot.add_commands({'Hello': hello, 'Product': (product, [int, int])})
my_bot.add_command(admin, admin=True)

# Commands were created manually
#my_bot.add_commands([cmd_hello, cmd_admin, cmd_product])


# Just functions was created
my_bot.add_listener(on_message)

# Listener were created manually
#my_bot.add_listener(listener_on_message)

my_bot.run()