"""
Miscellaneous methods and other variables
for the YrmyBot IRC bot framwork
"""


class colors:
    red = "\033[1;31m"
    green = "\033[1;32m"
    blue = "\033[0;34m"
    yellow = "\033[1;33m"
    cyan = "\033[1;36m"
    purple = "\033[1;35m"

    bold = "\033[;1m"
    reverse = "\033[;7m"
    reset = "\033[0m"


def testColors():

    print("{0}RED{1}".format(colors.red, colors.reset))
    print("{0}GREEN{1}".format(colors.green, colors.reset))
    print("{0}BLUE{1}".format(colors.blue, colors.reset))
    print("{0}YELLOW{1}".format(colors.yellow, colors.reset))
    print("{0}CYAN{1}".format(colors.cyan, colors.reset))
    print("{0}PURPLE{1}".format(colors.purple, colors.reset))
    print("{0}BOLD{1}".format(colors.bold, colors.reset))
    print("{0}REVERSE{1}".format(colors.reverse, colors.reset))
    print("{1}RED{0}{2}GREEN{0}{3}BLUE!{0}".format(colors.reset, colors.red, colors.green, colors.blue))
    print("NORMAL")


def clearfile(filepath):
    """Clears a file"""
    open(filepath, 'w').close()


if __name__ == "__main__":
    testColors()
