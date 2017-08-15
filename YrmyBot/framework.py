"""
IRC connection handler module
"""

import socket
from inspect import ismethod, getmembers

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
            'handle_message' ]
    commands = []

    def __init__(self, nickname, server, port=6667):
        # Set up variables
        self.nickname = nickname
        self.server = server
        self.port = port
        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel = ""
        
        # List all the non-framework functions into an array 
        functions = getmembers(self, predicate=ismethod)
        for x in functions:
            if x[0] not in self.framework_funcs:
                self.commands.append(x[0])

    def connect_to_server(self):
        """Establish a connection to the given IRC server"""
        self.connection_socket.connect((self.server, self.port))

        self.connection_socket.send(bytes("USER "  + self.nickname + " " + self.nickname + " "+ self.nickname + ":Testing... .\n" , "UTF-8"))
        self.connection_socket.send(bytes("NICK " + self.nickname + "\n", "UTF-8"))

    def identify(self, password):
        """Identify with the NickServ on the server with the right password (if needed)"""
        self.connection_socket.send(bytes("PRIVMSG NickServ :identify " + password +" \n", "UTF-8")) # Auth with server
    def join_channel(self, channel):
        """Join a channel on the connected IRC network"""
        self.connection_socket.send(bytes("JOIN %s\n" % channel, "UTF-8"))
        message = ""
        while message.find("End of /NAMES list") == -1:
            message = self.connection_socket.recv(2048).decode("UTF-8")
            message = message.strip('\n\r')
            print(message)
        self.channel = channel

    def ping_server(self):
        """Responding to ping messages received from the server to avoid disconnection"""
        self.connection_socket.send(bytes("PONG :pingis\n", "UTF-8"))
    
    def fetch_message(self):
        """Receive the message sent by the server"""
        message = self.connection_socket.recv(2048).decode("UTF-8")
        message = message.strip('\n\r')
        return message
    
    def send_message(self, message, target):
        """Send a message to a person or a channel"""
        self.connection_socket.send(bytes("PRIVMSG "+ target +  " :" + message + "\n" , "UTF-8"))

    def handle_message(self, message):
        """Handle the received message"""
        if message.find("PRIVMSG") != -1:
            print(message)
            # Someone sent a message (channel or private)

            name = message.split('!', 1)[0][1:]
            message_body = message.split('PRIVMSG', 1)[1].split(':', 1)[1]
            channel =  message.split('PRIVMSG', 1)[1].split(':', 1)[0].strip()
            
            print(name + " says: " + message_body + " @ " + channel)
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
                    print("command: %s not implemented" % command)
                    return

        elif message.find("PING :") != -1:
            # Received a ping from the server 
            self.ping()

        else:
            # Do nothing
            return
            
