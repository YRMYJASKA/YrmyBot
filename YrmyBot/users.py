"""
Manages the user file of all the users and their powerLevel.
PowerLevel determines if an user can execute certain commands
Powerlevel max. value = 100

Data is saved in format of:
'name powerLevel'
"""


def load_file(filepath="users.txt"):
    users = {}
    with open(filepath, 'r') as f:
        for line in f:
            if len(line) > 2:
                name = line.split('=')[0]
                powerlevel = line.split('=')[1]
                users[name.lower()] = powerlevel
        f.close()
    return users


def write_file(users, filepath="users.txt"):
    with open(filepath, 'w') as f:

        for name in users:
            f.write(name + "=" + users.get(name, 0) + "\n")
        f.close()
    return


def fetch_user(name, filepath="users.txt"):
    users = load_file(filepath)

    user = users.get(name, 0)

    write_file(users, filepath)
    return int(user)


def del_user(name, filepath="users.txt"):
    users = load_file(filepath)

    if name in users:
        del users[name]

    write_file(users, filepath)
    return


def add_user(name, powerlevel, filepath="users.txt"):
    users = load_file(filepath)

    if name in users:
        return "User already in record"
    else:
        users[name] = powerlevel

    write_file(users, filepath)
    return


def modify_user_powerlvl(name, powerlevel, filepath="users.txt"):

    users = load_file(filepath)

    if name in users:
        users[name] = powerlevel
    else:
        print("no name: %s in users" % name)

    write_file(users, filepath)
    return
