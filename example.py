# Usage: python3 example.py <Bot's name> <IRC server ip>

from YrmyBot.bot import Bot
import sys
import YrmyBot.misc


# Bot made using the YrmyBot framework
class MyBot(Bot):
    # This is a command which can be invoked with '!hello'
    def hello(self, user, message, channel):
        """Hello Test"""
        self.send_message("Hello!", channel)


# Clear logs
YrmyBot.misc.clearfile("raw.log")

myBot = MyBot(sys.argv[1], sys.argv[2])

print("Password for the bot")
print("(Leave empty if there is no indentification needed)")
password = input('> ')
chan = input("Channel to join: ")

# Connecting to server
myBot.connect_to_server()
if len(password) > 0:
    myBot.identify(password)
myBot.join_channel(chan)

while 1:
    myBot.handle_message(myBot.fetch_message())
