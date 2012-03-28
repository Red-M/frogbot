# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook
import os
import time
import re
from itertools import izip

@hook.command
def kl(inp, say=None, nick=None, input=None):
    "kill switch."
    inuserhost = input.user+'@'+input.host
    if not input.nick in bot.config["owner"]:
        input.notice("Only the bot owner can use this command!")
    elif input.nick in bot.config["owner"]:
        input.conn.send('QUIT :Kill switch activated by Red_M.')
        time.sleep(3)
        os.abort()

@hook.command
def rl(inp, say=None, input=None):
    "restart switch."
    inuserhost = input.user+'@'+input.host
    if (input.nick not in input.bot.config["admins"] and inuserhost not in input.bot.config["admins"]):
         input.notice("Only bot admins can use this command!")
    elif (input.nick in input.bot.config["admins"] or inuserhost in input.bot.config["admins"]):
       input.conn.send('QUIT :Restart switch activated by '+input.nick+'.')
       os.system("screen python2.6 ./bot.py")
       time.sleep(3)
       os.abort()


@hook.command
def nasf(inp, bot=None, input=None):
	"checks to see if the bot gives a fuck about what you asked..."
	inuserhost = input.user+'@'+input.host
	if input.nick in input.bot.config["admins"] or inuserhost in bot.config["admins"]:
		return" Multiple fucks found..."
	else:
		return" Not a single fuck was found...."

@hook.command("adm")
@hook.command
def admins(inp, bot=None, input=None):
	"tells the current admins of the bot..."
	outos=str(bot.config["admins"])
	outos=outos.replace("u'","")
	outos=outos.replace("'","")
	outos=outos.replace("[","")
	outos=outos.replace("]","")
	input.conn.send("PRIVMSG "+ input.chan +" :The Admins of this bot are: "+outos)

@hook.command
def users(inp, bot=None, input=None):
        outoss=(str(input.conn.users.users))
        outoss=outoss.replace("u'","")
        outoss=outoss.replace("'","")
        #comp = re.compile('^<User object at 0x1.*>$')
        #print str(comp) 
        outoss=outoss.replace("<User object at ","")
        outoss=outoss.replace("{","")
        outoss=outoss.replace(">,","")
        outoss=outoss.replace("}","")
        outoss=outoss.replace(": ","")

        input.say(str(outoss))

@hook.command("channels")
@hook.command
def chan(inp, input=None, db=None, bot=None, users=None):
	"lists the current channels that I am in..."
        outrs=str(users.channels.keys())
        outrs=outrs.replace("u'","")
        outrs=outrs.replace("'","")
        outrs=outrs.replace("[","")
        outrs=outrs.replace("]","")
        input.conn.send("PRIVMSG "+ input.chan +" :I am in these channels: "+outrs)
     
@hook.command
def raw(inp, input=None):
	"sends a raw irc command. bot owner only..."
	if input.nick in bot.config["owner"] and not inp=='':
		input.conn.send(inp)
	else:
		input.conn.send("PRIVMSG "+input.nick+" :You cannot do this.")
  

@hook.command
def gtfo(inp, input=None):
       "makes me leave the channel. can be used by a channel op or bot admin..."
       inuserhost = input.user+'@'+input.host
       if (input.nick in input.bot.config["admins"] or inuserhost in bot.config["admins"]) or "o" in users[input.chan].usermodes[input.nick]:
               input.conn.send("PART "+input.chan)
       else:
               input.conn.send("PRIVMSG "+input.nick+" :You cannot do this.")


@hook.event("KICK")
def kickss(inp, input=None):
    inuserhost = input.user+'@'+input.host
    if input.nick in input.bot.config['admins'] or inuserhost in bot.config["admins"]:
        return"WHY! WHY! WHY HIM?!?!?!? OH GOD WHY!"
    else:
        input.say("oh god!")
		
@hook.event("QUIT")
def quitss(inp, input=None):
    inuserhost = input.user+'@'+input.host
    if input.nick in input.bot.config['admins'] or inuserhost in bot.config["admins"]:
        input.say("*as Gir* Master, where did you go? I can't see you!")
    else:
        input.say("Bye!")


@hook.command
def ac(inp, input=None):
    "asks crow something."
    if not inp == "":
        input.conn.send("PRIVMSG crow :?" + inp + " > " + input.nick)
    if not input.nick in bot.config["owner"]:
        input.conn.send("PRIVMSG "+bot.config["owner"]+" :"+input.nick+" has asked crow ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.") 

@hook.command
def aw(inp, input=None):
    "asks wololo something."
    if not inp == "":
        input.conn.send("PRIVMSG wololo :?" + inp + " > " + input.nick)
    if not input.nick in bot.config["owner"]:
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
    if not input.nick in bot.config["owner"]:     
        input.conn.send("PRIVMSG "+bot.config["owner"]+" :"+input.nick+" has asked "+botn+" ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.")   