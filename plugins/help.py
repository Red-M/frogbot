import re

from util import hook


@hook.command(autohelp=False)
def help(inp, bot=None, pm=None):
    ".help [command] -- gives a list of commands/help for a command"

    funcs = {}
    disabled = bot.config.get('disabled_plugins', [])
    disabled_comm = bot.config.get('disabled_commands', [])
    for command, (func, args) in bot.commands.iteritems():
        fn = re.match(r'^plugins.(.+).py$', func._filename)
        if fn.group(1).lower() not in disabled:
            if command not in disabled_comm:
                if func.__doc__ is not None:
                    if func in funcs:
                        if len(funcs[func]) < len(command):
                            funcs[func] = command
                    else:
                        funcs[func] = command

    commands = dict((value, key) for key, value in funcs.iteritems() if key not in ["8ballnooxt"])
    if not inp:
        length = 0
        out = ["", ""]
        well = []
        for x in commands:
            well.append(x)
        well.sort()
        for x in well:
            if len(out[0]) + len(str(x)) > 405:
                out[1] += " " + str(x)
            else:
                out[0] += " " + str(x)

        pm("available commands: " + out[0][1:])
        if out[1]:
            pm(out[1][1:])
    else:
        if inp in commands:
            pm(commands[inp].__doc__)
