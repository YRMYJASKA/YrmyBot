"""
Logging module for YrmyBot

Console and to file logging
"""
from .misc import colors
from sys import exit
from time import localtime, strftime


def consoleLog(msg, logType):
    """Outputs a message to the console"""
    if logType == "WARN":
        prefix = "{0}[WARN]{1}".format(colors.yellow, colors.reset)
    elif logType == "INFO":
        prefix = "{0}[INFO]{1}".format(colors.cyan, colors.reset)
    elif logType == "FATAL":
        prefix = "{0}[FATAL]{1}".format(colors.red, colors.reset)
    elif logType == "INTERNAL":
        prefix = "{0}[INTERNAL]{1}".format(colors.blue, colors.reset)
    elif logType == "CHAT":
        prefix = "{0}[CHAT]{1}".format(colors.green, colors.reset)
    elif logType == "NOTE":
        prefix = "{0}[NOTE]{1}".format(colors.purple, colors.reset)
    elif logType == "EMPTY":
        prefix == ""
    else:
        consoleLog("Invalid value passed on to consoleLog()", "INTERNAL")
        return

    timeStamp = strftime("%H:%M:%S", localtime())
    msg = timeStamp + " " + prefix + msg
    print(msg)
    if logType == "FATAL":
        exit(-1)


def rawLog(line, filepath="raw.log"):
    with open(filepath, "a") as f:
        f.write(line)
        f.close()
