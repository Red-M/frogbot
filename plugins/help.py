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
        out = ["", "", "", ""]
        well = []
        for x in commands:
            well.append(x)
        well.sort()
        out[0] += "available commands:"
        for x in well:
            if len(out[0]) + len(str(x)) < 300:
                out[0] += " " + str(x)
            else:
                if len(out[0]) + len(str(x)) < 300:
                    out[1] += " " + str(x)
                else:
                    if len(out[1]) + len(str(x)) < 300:
                        out[2] += " " + str(x)
                    else:
                        if len(out[2]) + len(str(x)) < 300:
                            out[3] += " " + str(x)

        pm(out[0][0:])
        if out[1]:
            pm(out[1][1:])
        if out[2]:
            pm(out[2][1:])
        if out[3]:
            pm(out[3][1:])
        pm("This bot also has auto link titling with shortening with the auto titling, rate limiting commands and a permissions system.")
    else:
        if inp in commands:
            pm(commands[inp].__doc__)
