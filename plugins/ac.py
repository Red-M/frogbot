# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook
import os
import sys
import time
import re
from itertools import izip
from util import perm

@hook.command
def kl(inp, say=None, nick=None, input=None):
    "kill switch."
    if not perm.isowner(input):
        input.notice("Only the bot owner can use this command!")
    elif not perm.isowner(input):
        input.conn.send('QUIT :Kill switch activated by Red_M.')
        time.sleep(3)
        sys.exit()

@hook.command
def rl(inp, say=None, input=None, bot=None):
    "restart switch."
    if not perm.isadmin(input):
        input.notice("Only bot admins can use this command!")
    elif perm.isadmin(input):
        input.conn.send('QUIT :Restart switch activated by '+input.nick+'.')
        if os.name == 'posix':
            os.system("screen python ./bot.py")
            time.sleep(3)
            sys.exit()
        elif os.name == 'nt':
            os.system(bot.config["restartcmd"])
            time.sleep(3)
            sys.exit()

@hook.command
def nasf(inp, bot=None, input=None):
	"checks to see if the bot gives a fuck about what you asked..."
	if perm.isadmin(input):
		return" Multiple fucks found..."
	else:
		return" Not a single fuck was found...."

@hook.command("adm")
@hook.command
def admins(inp, bot=None, input=None):
	"tells the current admins of the bot..."
	outos=', '.join(bot.config["admins"])
	input.conn.send("PRIVMSG "+ input.chan +" :The Admins of this bot are: "+outos)

@hook.command
def users(inp, bot=None, input=None):
    input.say(" ".join(input.conn.users.users))

@hook.command("channels")
@hook.command
def chan(inp, input=None, db=None, bot=None, users=None):
    "lists the current channels that I am in..."
    outrs=', '.join(users.channels.keys())
    input.conn.send("PRIVMSG "+ input.chan +" :I am in these channels: "+outrs)
     
@hook.command
def raw(inp, input=None):
	"sends a raw irc command. bot owner only..."
	if perm.isowner(input):
		input.conn.send(inp)
	else:
		input.conn.send("PRIVMSG "+input.nick+" :You cannot do this.")
  

@hook.command
def gtfo(inp, input=None):
    "makes me leave the channel. can be used by a channel op or bot admin..."
    if perm.isadmin(input) or "o" in users[input.chan].usermodes[input.nick]:
        input.conn.send("PART "+input.chan)
    else:
        input.conn.send("PRIVMSG "+input.nick+" :You cannot do this.")


@hook.event("KICK")
def kickss(inp, input=None):
    if perm.isadmin(input):
        return input.nick+": WHY! WHY! WHY HIM?!?!?!? OH GOD WHY!"
    else:
        input.say("oh god!")

@hook.event("QUIT")
def quitss(inp, input=None, bot=None):
    on=0
    if on==1:
        if perm.isadmin(input):
            input.say("*as Gir* Master, where did you go? I can't see you!")
        else:
            input.say("Bye!")
		
@hook.event("PART")
def partss(inp, input=None, bot=None):
    on=0
    if on==1:
        if perm.isadmin(input):
            input.say("*as Gir* Master, where did you go? I can't see you!")
        else:
            input.say("Bye!")

@hook.event("JOIN")
def joinss(inp, input=None, bot=None):
    on=0
    if on==1:
        if perm.isadmin(input):
            input.say("*as Gir* ooh Hi Master!")
        else:
            if input.nick==input.conn.nick:
                input.say("")
            else:
                input.say("Hi there.")


@hook.command
def ac(inp, input=None):
    "asks crow something."
    if not inp == "":
        input.conn.send("PRIVMSG crow :?" + inp + " > " + input.nick)
    if not perm.isowner(input):
        input.conn.send("PRIVMSG "+bot.config["owner"]+" :"+input.nick+" has asked crow ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.") 

@hook.command
def aw(inp, input=None):
    "asks wololo something."
    if not inp == "":
        input.conn.send("PRIVMSG wololo :?" + inp + " > " + input.nick)
    if not perm.isowner(input):
        input.conn.send("PRIVMSG "+bot.config["owner"]+" :"+input.nick+" has asked wololo ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.") 

@hook.command
def ab(inp, input=None):
    ".ab <botnick> <factoid> -- asks <botnick> <factoid>."
    if not inp == "":
        botn = inp.split(" ")
        botn = botn[0]
        input.conn.send("PRIVMSG "+botn+" :?" + inp + " > " + input.nick)  
    if not perm.isowner(input):     
        input.conn.send("PRIVMSG "+bot.config["owner"]+" :"+input.nick+" has asked "+botn+" ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.")   