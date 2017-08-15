"""
The Bot module
"""

from .framework import BotFramework
from .users import *
class Bot(BotFramework):
    """The main bot class"""
    
    exitmsg = "Exiting..."
    
    # Admin commands:
    def shutdown(self, user, message, channel):
        """(ADMIN)Shutdowns the bot"""
        if fetch_user(user) >= 100:
            self.send_message(self.exitmsg, channel)
            self.connection_socket.send(bytes("QUIT \n", "UTF-8"))
        else:
            self.send_message("PowerLevel too low!", user)
    def add_user(self, user, message, channel):
        """(ADMIN)Adds a user to the record. Usage: !add_user <name> <power_level>"""
        if len(message.split(' ')) < 3:
            print("Not enough arguments!")
            return
        if fetch_user(user) >= 100:
            add_user(message.split(' ')[1], message.split(' ')[2])
        if fetch_user(user) >= 50 and int(message.split(' ')[2]) < 51:
            add_user(message.split(' ')[1], message.split(' ')[2])
        else:
            self.send_message("PowerLevel too low!", user)
    def del_user(self, user, message, channel):
        """(ADMIN)Deletes a user from the record. Usage !del_user <name>"""
        if len(message.split(' ')) < 2:
            print("Not enough arguments!")
            return
        if fetch_user(user) >= 100:
            del_user(message.split(' ')[1])
        else:
            self.send_message("PowerLevel too low!", user)
    def modify_user(self, user, message, channel):
        if len(message.split(' ')) < 3:
            print("Not enough arguments!")
            return
        """(ADMIN)Modifies a user from in record. Usage !modify_user <name> <new power_level>"""
        if fetch_user(user) >= 100:
            modify_user_powerlevel(message.split(' ')[1], message.split(' ')[2])
        else:
            self.send_message("PowerLevel too low!", user)
    # Standard commands
    def github(self, user, message, channel):
        self.send_message("Source code for YrmyBot: https://github.com/yrmyjaska/YrmyBot")
    def ping(self, user, message, channel):
        """The bot will respond 'pong!'"""
        self.send_message("pong!", channel)

    def help(self, user, message, channel):
        """Lists all the commands available on the bot"""
        self.send_message("List of all commands:", user)
        line = ""
        spacing = 12
        for x in self.commands:
            line = x
            for i in range(0, spacing - len(x)):
                line += " "
            self.send_message("    %s- %s" % (line, getattr(self, x).__doc__), user)


