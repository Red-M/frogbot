#  Shitty plugin made by iloveportalz0r
#  Broken by The Noodle
#  Improved by Lukeroge
#  edited for frog by Red-M on github or Red_M on esper.net
from util import hook
from util import perm

# Added to make the move to a new auth system a lot easier
# Improved to account for frog's permissions system and moved the improvement to perm.py

@hook.command
def join(inp, input=None, db=None, notice=None):
    ".join <channel> -- joins a channel"
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    notice("Attempting to join " + inp + "...")
    input.conn.send("JOIN " + inp)

@hook.command
def cycle(inp, input=None, db=None, notice=None):
    ".cycle <channel> -- cycles a channel"
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    notice("Attempting to cycle " + inp + "...")
    input.conn.send("PART " + inp)
    input.conn.send("JOIN " + inp)

@hook.command
def part(inp, input=None, notice=None):
    ".part <channel> -- leaves a channel"
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    notice("Attempting to part from " + inp + "...")
    input.conn.send("PART " + inp)

@hook.command
def nick(inp, input=None, notice=None):
    ".nick <nick> -- change the bots nickname to <nick>"
    if not input.nick in input.bot.config["owner"]:
        notice("Only the bot owner can use this command!")
        return
    notice("Changing nick to " + inp + ".")
    input.conn.send("NICK " + inp)

@hook.command
def kick(inp, input=None, notice=None):
    ".kick [channel] <user> [reason] -- kick a user!"
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    split = inp.split(" ")
    if split[0][0] == "#":
        chan = split[0]
        user = split[1]
        out = "KICK %s %s" % (chan, user)
        if len(split) > 2:
            reason = ""
            for x in split[2:]:
                reason = reason + x + " "
            reason = reason[:-1]
            out = out+" :"+reason
    else:
        chan = input.chan
        user = split[0]
        out = "KICK %s %s" % (input.chan, split[0])
        if len(split) > 1:
            reason = ""
            for x in split[1:]:
                reason = reason + x + " "
            reason = reason[:-1]
            out = out + " :" + reason

    notice("Attempting to kick %s from %s..." % (user, chan))         
    input.conn.send(out)

@hook.command
def say(inp, input=None, notice=None):
    ".say [channel] <message> -- makes the bot say <message> in [channel]. if [channel] is blank the bot will say the <message> in the channel the command was used in."
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    split = inp.split(" ")
    if split[0][0] == "#":
        message = ""
        for x in split[1:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :%s" % (split[0], message)
    else:
        message = ""
        for x in split[0:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :%s" % (input.chan, message)
    input.conn.send(out)

@hook.command("me")
@hook.command
def act(inp, input=None, notice=None):
    ".act [channel] <action> -- makes the bot act <action> in [channel]. if [channel] is blank the bot will act the <action> in the channel the command was used in."
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    split = inp.split(" ")
    if split[0][0] == "#":
        message = ""
        for x in split[1:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION \x01\x034,1 %s\x01" % (split[0], message)
    else:
        message = ""
        for x in split[0:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION \x034,1 %s\x01" % (input.chan, message)
    input.conn.send(out)

@hook.command
def topic(inp, input=None, notice=None):
    ".topic [channel] <topic> -- change the topic of a channel"
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    split = inp.split(" ")
    split[0] = split[0]+ " :"
    lenchan = len(split[0])
    print lenchan+1
    split = str(' '.join(split))
    print split[0][0]
    if split[0][0] == "#":
        if testsf==True:
            out = "TOPIC %s" % (split)
    else:
        if testsf=="":
            out = "PRIVMSG %s :Cant set topic." % (input.nick)
        else:
            out = "PRIVMSG "+input.nick+" :Cant set topic. Not enough arguements in command." 
    input.conn.send(out)
