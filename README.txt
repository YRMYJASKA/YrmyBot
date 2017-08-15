YrmyBot
--------------------------------------------------------
REQUIREMENTS:
  - python 3+
--------------------------------------------------------
INSTALLING:
  1. Move to your working directory
  2. git clone https://github.com/YRMYJASKA/YrmyBot .
     
     This will clone the git rep. of YrmyChat into your working directory
     (Dont forget the dot at the end!)
  3. Start Programming! See example.py and section "HOW TO USE" for help.
--------------------------------------------------------
HOW TO USE: 
example code from 'example.py' (modified a bit to make it simpler)

      from YrmyBot.bot import Bot 

      # Bot made using the YrmyBot framework
      class MyBot(Bot):
          # This is a user made command which can be invoked with '!hello'
          def hello(self, user, message, channel):
              """Hello Test"""
              self.send_message("Hello!", channel)

      myBot = MyBot("BertTheBot","irc.freenode.net")
     
      password = "SUPERSECRETPASSWORD12345"
      chan = "#MyVeryOwnChannel"

      # Connecting to server
      myBot.connect_to_server()
      myBot.identify(password)
      myBot.join_channel(chan)

      while 1:
      myBot.handle_message(myBot.fetch_message())

This is a very simple bot that will join to a server located in "irc.freenode.net" 
and join a channel called "#MyVeryOwnChannel". Also it will identify for the NickServ service
if there is an account made for the bot with the given password.

Then it will go to the main loop of the program.
The program can be cancelled by pressing Ctrl-C in the terminal.

The commands for this bot are defined in the declaration of MyBot.
Here a commnad called hello is defined and if someone sends a message directly or 
via a channel to the bot tthe bot will respond "Hello!"
New commands can be defined by just defining a method in a class which inherits from Bot and 
adding a """ """ docstring to add a help comment.


To see all the commands defined call the command "!help" to the bot
