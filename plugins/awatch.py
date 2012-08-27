# auto watch written by Red-M on github or Red_M on esper.net
from util import hook, perm, munge
import json

@hook.sieve
def awatch(bot, input, func, kind, args):
    repchan = ''.join(input.conn.conf["reportchan"]) #the channel to report back to
    cmdpre = "," #your cmd prefix
    ignorenick=''.join(input.conn.conf["owner"])
    nickf = munge.munge(0, input, bot, 0, "")
    cmduse = (sorted(bot.commands))
    cmdign=",auth"
    cmdign2="auth"
    #print(input.lastparam)
    if kind=="command" and not perm.isowner(input) and not input.lastparam.startswith(cmdign) and not input.lastparam.startswith(cmdign2):
        cmdused = input.trigger
        if input.lastparam==",stfu" or input.lastparam==",ignore":
            input.conn.send("PRIVMSG "+repchan+" :I have been muted in "+input.chan+" by "+nickf+input.mask)
        if input.lastparam==",kthx" or input.lastparam==",listen":
            input.conn.send("PRIVMSG "+repchan+" :I have been unmuted in "+input.chan+" by "+nickf+input.mask)
        if input.lastparam==",join":
            input.conn.send("PRIVMSG "+repchan+" :I have joined "+input.chan+" as told to by "+nickf+input.mask)
        if input.lastparam==",part" or input.lastparam==",gtfo":
            input.conn.send("PRIVMSG "+repchan+" :I have left "+input.chan+" as told to by "+nickf+input.mask)
        if input.chan==input.nick and not perm.isowner(input) and cmdused in cmduse and not input.lastparam.startswith(cmdign):#cmd use in a private msg
            input.conn.send("PRIVMSG "+repchan+" :"+nickf+input.mask+" (used/tried to use) "+input.lastparam+" in a private message.")
        if input.chan.startswith("#") and not input.chan==repchan and not perm.isowner(input) and cmdused in cmduse and  not input.lastparam.startswith(cmdign):#cmd use in a channel
            input.conn.send("PRIVMSG "+repchan+" :"+nickf+input.mask+" (used/tried to use) "+input.lastparam+" in "+input.chan)
        if input.chan==repchan and not perm.isowner(input) and cmdused in cmduse and not input.lastparam.startswith(cmdign):#cmd use in the report chan which is sent back to the owner.
            input.conn.send("PRIVMSG "+ignorenick+" :"+input.nick+input.mask+" (used/tried to use) "+input.lastparam+" in "+repchan)
    elif (not perm.isowner(input)) and ((input.lastparam.startswith("?") and not input.lastparam=="?") or (input.lastparam.startswith("!") and not input.lastparam=="!")):
        if (input.command=="PRIVMSG" and not input.lastparam in cmduse):
            if input.chan==input.nick and not perm.isowner(input):#factoids in a privmsg
                input.conn.send("PRIVMSG "+repchan+" :"+nickf+input.mask+" asked me "+input.lastparam+" in a private message.")
        elif not input.lastparam.startswith(cmdign):
            input.conn.send("PRIVMSG "+repchan+" :"+nickf+input.mask+" asked me "+input.lastparam+" in "+input.chan)
    return input


@hook.event("KICK")
def kickss(inp, input=None, bot=None):
    repchan = input.conn.conf["reportchan"]
    nickf = munge.munge(0, input, bot, 0, "")
    json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=1)
    if input.nick==input.conn.nick and not perm.isowner(input) and not perm.isbot(input):
        input.conn.conf['channels'].remove(input.inp)
        input.conn.send("PRIVMSG "+repchan+" :I have been kicked in "+input.chan+" by "+nickf)

@hook.event('INVITE')
def invite(paraml, conn=None, input=None, bot=None):
    repchan = input.conn.conf["reportchan"]
    nickf = munge.munge(0, input, bot, 0, "")
    if not perm.isowner(input) and not perm.isignored(input) and not perm.isbot(input):
        input.conn.send("PRIVMSG "+repchan+" :I have been invited to "+paraml[-1]+" by "+nickf)

@hook.event('JOIN')
def joins(paraml, conn=None, input=None, bot=None):
    repchan = input.conn.conf["reportchan"]
    if not perm.isowner(input) and not perm.isignored(input) and not perm.isbot(input) and input.nick==conn.nick:
        input.conn.send("PRIVMSG "+repchan+" :I have joined "+paraml[-1])
