from util import hook
import usertracking
import time

@hook.sieve
def stfusieve(bot, input, func, kind, args):
    if kind == "event": #log, usertracking, etc use event
        return input
    if "chan" in input.keys() and input.chan in input.conn.users.channels and hasattr(input.conn.users[input.chan], "stfu"):
        if input.command=="PRIVMSG" and input.lastparam[1:]=="kthx":
            return input
        else:
            return None
    return input

@hook.command
def stfu(inp, input=None, db=None, bot=None, users=None):
    if inp and inp in input.conn.users.channels.keys():
        input.chan=inp
    if usertracking.query(db, bot.config, input.nick, input.chan, "stfu") or "o" in users[input.chan].usermodes[input.nick]:
        users[input.chan].stfu="%s %d" % (input.nick, time.time())
        input.notice("I am now muted here.")
    else:
        input.notice("you don't have permission to do that")

@hook.command
def kthx(inp, input=None, db=None, bot=None, users=None):
    if inp and inp in users.channels.keys():
        input.chan=inp
    if usertracking.query(db, bot.config, input.nick, input.chan, "stfu") or "o" in users[input.chan].usermodes[input.nick]:
        if hasattr(users[input.chan], "stfu"):
            input.notice("I am no longer muted here.")
            del users[input.chan].stfu
        else:
            input.notice("I am not muted here.")
    else:
        input.notice("you don't have permission to do that")