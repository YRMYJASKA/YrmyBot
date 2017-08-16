"""
The Bot module
"""

from .framework import BotFramework
from .users import add_user, del_user, modify_user_powerlvl, fetch_user
import sys
from . import logging


class Bot(BotFramework):
    """The main bot class"""

    exitmsg = "Exiting..."

    # Admin commands:
    def shutdown(self, user, message, channel):
        """(ADMIN)Shutdowns the bot"""

        if fetch_user(user) >= 100:
            self.send_message(self.exitmsg, channel)

            self.conn_socket.send(bytes("QUIT \n", "UTF-8"))
            msg = "{0} shutdown by '{1}'".format(self.nickname, user)
            logging.consoleLog(msg, "INFO")

            sys.exit(0)
        else:
            self.send_message("PowerLevel too low!", user)

            msg = "{0} tried to shutdown the bot".format(user)
            logging.consoleLog(msg, "NOTE")

    def add_user(self, user, message, channel):
        """(ADMIN)Adds a user to file. Usage: !add_user <name> <power_level>"""

        if len(message.split(' ')) < 3:
            self.send_message("Not enough arguments!", channel)
            return
        if fetch_user(user) >= 100:
            name = message.split(' ')[1]
            powerlvl = message.split(' ')[2]
            add_user(name, powerlvl)

            msg = "User '{0}' with PL of {1} was added!".format(name, powerlvl)
            logging.consoleLog(msg, "INFO")
        else:
            self.send_message("PowerLevel too low!", user)

    def del_user(self, user, message, channel):
        """(ADMIN)Deletes a user from the file. Usage !del_user <name>"""

        if len(message.split(' ')) < 2:
            print("Not enough arguments!")
            return
        if fetch_user(user) >= 100:
            name = message.split(' ')[1]
            del_user(name)

            msg = "User '{0}' was deleted".format(name)
            logging.consoleLog(msg, "INFO")
        else:
            self.send_message("PowerLevel too low!", user)

    def modify_user(self, user, message, channel):
        """(ADMIN)Modify user in file. Usage !modify_user <name> <power_lvl>"""

        if len(message.split(' ')) < 3:
            print("Not enough arguments!")
            return
        if fetch_user(user) >= 100:
            name = message.split(' ')[1]
            powerlvl = message.split(' ')[2]
            modify_user_powerlvl(name, powerlvl)

            msg = "User '{0}' was modified".format(name)
            logging.consoleLog(msg, "INFO")
        else:
            self.send_message("PowerLevel too low!", user)

    # Standard commands
    def github(self, user, message, channel):
        """Sends the link to the source code on github.com"""

        msg = "Source code for YrmyBot: https://github.com/yrmyjaska/YrmyBot"
        self.send_message(msg, channel)

    def ping(self, user, message, channel):
        """The bot will respond with 'pong!'"""

        self.send_message("pong!", channel)

    def help(self, user, message, channel):
        """Lists all the commands available on the bot"""

        self.send_message("List of all commands:", user)
        line = ""
        spacing = 12
        for command in self.commands:
            line = command
            # Even spacing
            for i in range(0, spacing - len(command)):
                line += " "
            comment = getattr(self, command).__doc__
            self.send_message("    %s- %s" % (line, comment), user)
