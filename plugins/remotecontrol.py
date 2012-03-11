# Shitty plugin made by iloveportalz0r

from util import hook

@hook.command
def join(inp, input=None):
    ".join <channel>"
    if input.nick not in input.bot.config["admins"]:
        return "Only bot admins can use this command!"
    chan = inp.split(' ', 1)
    #if len(chan) != 1:
        #return "Usage: omg please join <channel>"
    input.say("Joining " + inp)
    input.conn.send("JOIN " + inp)

@hook.command
def part(inp, input=None):
    ".part <channel> - Leave a channel"
    if input.nick not in input.bot.config["admins"]:
        return "Only bot admins can use this command!"
    chan = inp.split(' ', 1)
    #if len(chan) != 1:
        #return "Usage: omg please part <channel>"
    input.say("Parting from " + inp + " D:")
    input.conn.send("PART " + inp)

@hook.command
def chnick(inp, input=None):
    ".chnick <nick> - Change the nick!"
    if input.nick not in input.bot.config["admins"]:
        return "Only bot admins can use this command!"
    chan = inp.split(' ', 1)
    #if len(chan) != 1:
        #return "Usage: omg please part <channel>"
    input.say("Changing nick to " + inp)
    input.conn.send("NICK " + inp)