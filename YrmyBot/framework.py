"""
IRC connection handler module
"""

import socket
from inspect import ismethod, getmembers
from . import logging


class BotFramework(object):
    """The IRC connection and framework for the bot"""

    # Separate framework functions and user implemented commands
    framework_funcs = [
        "__init__",
        'connect_to_server',
        'identify',
        'join_channel',
        'ping_server',
        'fetch_message',
        'send_message',
        'handle_message']
    commands = []

    def __init__(self, nickname, server, port=6667):

        # Set up variables
        self.nickname = nickname
        self.server = server
        self.port = port
        self.conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel = ""
        self.passwordGiven = False

        # List all the non-framework functions into an array
        functions = getmembers(self, predicate=ismethod)
        for function in functions:
            if function[0] not in self.framework_funcs:
                self.commands.append(function[0])

        # Log event
        msg = "{0} was created for {1}:{2}".format(nickname, server, port)
        logging.consoleLog(msg, "INFO")

    def connect_to_server(self):
        """Establish a connection to the given IRC server"""

        self.conn_socket.connect((self.server, self.port))

        line = "USER {0} {0} {0} {0}:Bot\n".format(self.nickname)
        self.conn_socket.send(bytes(line, "UTF-8"))

        line = "NICK " + self.nickname + "\n"
        self.conn_socket.send(bytes(line, "UTF-8"))

        message = ""
        while message.find("End of /MOTD command") != -1:

            message = self.conn_socket.recv(2048).decode("UTF-8")
            message = message.strip('\n\r')

            # Log the raw input to the log
            logging.rawLog(message)

        # Log event
        msg = "Connecting to " + self.server
        logging.consoleLog(msg, "INFO")

    def identify(self, password):
        """Identify with the NickServ (if needed)"""

        msg = "Identifying with NickServ..."
        logging.consoleLog(msg, "INFO")

        line = "PRIVMSG NickServ :identify " + password + " \n"
        self.conn_socket.send(bytes(line, "UTF-8"))

        self.passwordGiven = True

    def join_channel(self, channel):
        """Join a channel on the connected IRC network"""

        line = "JOIN %s\n" % channel
        self.conn_socket.send(bytes(line, "UTF-8"))
        message = ""
        while message.find("End of /NAMES list") == -1:

            registered = message.find("This nickname is registered") != -1
            if registered and not self.passwordGiven:
                msg = self.nickname + " is already registered this server!"
                logging.consoleLog(msg, "FATAL")

            message = self.conn_socket.recv(2048).decode("UTF-8")
            # message = message.strip('\n\r')

            # Log the raw input to the log
            logging.rawLog(message)

        self.channel = channel

        msg = "joined channel {0}".format(channel)
        logging.consoleLog(msg, "INFO")

    def ping_server(self):
        """Respond to server pings"""

        line = "PONG :pingis\n"
        self.conn_socket.send(bytes(line, "UTF-8"))
        logging.consoleLog("Responded to Server's ping", "INFO")

    def fetch_message(self):
        """Receive the message sent by the server"""

        message = self.conn_socket.recv(2048).decode("UTF-8")
        message = message.strip('\n\r')

        logging.rawLog(message)
        return message

    def send_message(self, message, target):
        """Send a message to a person or a channel"""

        line = "PRIVMSG " + target + " :" + message + "\n"
        self.conn_socket.send(bytes(line, "UTF-8"))

    def handle_message(self, message):
        """Handle the received message"""

        if message.find("PRIVMSG") != -1:
            # Someone sent a message (channel or private)

            name = message.split('!', 1)[0][1:]
            message_body = message.split('PRIVMSG', 1)[1].split(':', 1)[1]
            channel = message.split('PRIVMSG', 1)[1].split(':', 1)[0].strip()

            msg = "{0} [{1}]: {2}".format(name, channel, message_body)
            logging.consoleLog(msg, "CHAT")

            if message_body[0] == '!':
                # A command was issued
                command = message_body.split(" ")[0][1:]

                # If the command was issued privately, respond
                # to the user instead to the bot itself
                if channel == self.nickname:
                    channel = name

                # Check if the command is even a command
                if command in self.commands:
                    command_to_call = getattr(self, command)

                    # All commands must follow the same
                    # argument structure. (user, message, channel)
                    command_to_call(name, message_body, channel)
                else:
                    msg = "No command called '{0}' implemented".format(command)
                    logging.consoleLog(msg, "NOTE")
                    return
        elif message.lower().find("invalid password") != -1:
            msg = "Invalid password set for {0}!".format(self.nickname)
            logging.consoleLog(msg, "FATAL")
        elif message.find("PING :") != -1:
            # Received a ping from the server
            self.ping_server()

        else:
            # Do nothing
            return
