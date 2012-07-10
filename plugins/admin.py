#  Shitty plugin made by iloveportalz0r
#  Broken by The Noodle
#  Improved by Lukeroge
#  edited for frog by Red-M on github or Red_M on esper.net
from util import hook, perm
import json

# Added to make the move to a new auth system a lot easier
# Improved to account for frog's permissions system and moved
# the improvement to plugins/util/perm.py

@hook.command
def join(inp, input=None, db=None, notice=None, bot=None):
    ".join <channel> -- joins a channel"
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    notice("Attempting to join %s..." % (inp))
    input.conn.send("JOIN %s" % (inp))
    if input.conn.conf['channels'].count(inp)==0:
        input.conn.conf['channels'].append(inp)
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=1)
        return"Done."

@hook.command
def cycle(inp, input=None, db=None, notice=None):
    ".cycle <channel> -- cycles a channel"
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    notice("Attempting to cycle %s..." % (inp))
    input.conn.send("PART %s" % (inp))
    input.conn.send("JOIN " % (inp))

@hook.command
def part(inp, input=None, notice=None, bot=None):
    ".part <channel> -- leaves a channel"
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    notice("Attempting to part from %s..."  % (inp))
    input.conn.send("PART %s" % (inp))
    if input.conn.conf['channels'].count(inp)==1:
        input.conn.conf['channels'].remove(inp)
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=1)
        return"Done."

@hook.command
def nick(inp, input=None, notice=None):
    ".nick <nick> -- change the bots nickname to <nick>"
    if not perm.isowner(input):
        notice("Only the bot owner can use this command!")
        return
    notice("Changing nick to %s."  % (inp))
    input.conn.send("NICK %s" % (inp))

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
            out = "%s :%s" % (out,reason)
    else:
        chan = input.chan
        user = split[0]
        out = "KICK %s %s" % (input.chan, split[0])
        if len(split) > 1:
            reason = ""
            for x in split[1:]:
                reason =  "%s%s " % (reason, x)
            reason = reason[:-1]
            out = "%s :%s" % (out,reason)

    notice("Attempting to kick %s from %s..." % (user, chan))
    input.conn.send(out)

@hook.command
def say(inp, input=None, notice=None):
    ".say [channel] <message> -- makes the bot say <message> in "
    "[channel]. if [channel] is blank the bot will say the <message> "
    "in the channel the command was used in."
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return None
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
    ".act [channel] <action> -- makes the bot act <action> in "
    "[channel]. if [channel] is blank the bot will act the <action> "
    "in the channel the command was used in."
    if not perm.isadmin(input):
        notice("Only bot admins can use this command!")
        return
    split = inp.split(" ")
    if split[0][0] == "#":
        message = ""
        for x in split[1:]:
            message = "%s%s " % (message, x)
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION \x01 %s\x01" % (split[0], message)
    else:
        message = ""
        for x in split[0:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION %s\x01" % (input.chan, message)
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
    split = str(' '.join(split))
    if split[0][0] == "#":
        if testsf==True:
            out = "TOPIC %s" % (split)
    else:
        if testsf=="":
            out = "PRIVMSG %s :Cant set topic." % (input.nick)
        else:
            out = "PRIVMSG "+input.nick+" :Cant set topic. "
            "Not enough arguements in command." 
    input.conn.send(out)
	
@hook.command
def ban(inp, conn=None, chan=None, notice=None, input=None):
    if perm.isadmin(input):
        inp = inp.split(" ")
        if inp[0][0] == "#":
            chan = inp[0]
            user = inp[1]
            out = "MODE %s +b %s" % (chan, user)
        else:
            user = inp[0]
            out = "MODE %s +b %s" % (chan, user)
        notice("Attempting to ban %s from %s..." % (user, chan))
        conn.send(out)


@hook.command(adminonly=True)
def unban(inp, conn=None, chan=None, notice=None, input=None):
    if perm.isadmin(input):
        inp = inp.split(" ")
        if inp[0][0] == "#":
            chan = inp[0]
            user = inp[1]
            out = "MODE %s -b %s" % (chan, user)
        else:
            user = inp[0]
            out = "MODE %s -b %s" % (chan, user)
        notice("Attempting to unban %s from %s..." % (user, chan))
        conn.send(out)

@hook.command
def kickban(inp, chan=None, conn=None, notice=None, input=None):
    if perm.isadmin(input):
        inp = inp.split(" ")
        if inp[0][0] == "#":
            chan = inp[0]
            user = inp[1]
            out1 = "MODE %s +b %s" % (chan, user)
            out2 = "KICK %s %s" % (chan, user)
            if len(inp) > 2:
                reason = ""
                for x in inp[2:]:
                    reason = reason + x + " "
                reason = reason[:-1]
                out = out + " :" + reason
        else:
            user = inp[0]
            out1 = "MODE %s +b %s" % (chan, user)
            out2 = "KICK %s %s" % (chan, user)
            if len(inp) > 1:
                reason = ""
                for x in inp[1:]:
                    reason = reason + x + " "
                reason = reason[:-1]
                out = out + " :" + reason

        notice("Attempting to kickban %s from %s..." % (user, chan))
        conn.send(out1)
        conn.send(out2)

@hook.command
def mode(inp, conn=None, chan=None, notice=None, input=None):
    if perm.isadmin(input):
        inp = inp.split(" ")
        if inp[0][0] == "#":
            chan = inp[0]
            user = inp[1]
            inpmode = inp[2]
            out = "MODE %s %s %s" % (chan, inpmode, user)
        else:
            chan = input.chan
            user = inp[0]
            inpmode = inp[1]
            out = "MODE %s %s %s" % (chan, inpmode, user)
        notice("Attempting to add the flag %s in %s to "
                                "%s..." % (inpmode, chan, user))
        conn.send(out)