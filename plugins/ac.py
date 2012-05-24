# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook, perm
import time
import dircache

@hook.command
def nasf(inp, bot=None, input=None):
	"checks to see if the bot gives a fuck about what you asked..."
	if perm.isadmin(input):
		return input.nick+": Multiple fucks found about"+input.inp
	else:
		return input.nick+": Not a single fuck was found about"+input.inp

@hook.command
def ac(inp, input=None, bot=None):
    "asks crow something."
    if isowner(input):
        if not inp == "":
            input.conn.send("PRIVMSG crow :?" + inp + " > " + input.nick)
        if not perm.isowner(input):
            input.conn.send("PRIVMSG "+input.conn.conf["owner"]+" :"+input.nick+" has asked crow ?" + inp + " > " + input.nick)
        if inp == "":
            input.say("nothing has been asked. not sending.") 

@hook.command
def aw(inp, input=None, bot=None):
    "asks wololo something."
    if not inp == "":
        input.conn.send("PRIVMSG wololo :?" + inp + " > " + input.nick)
    if not perm.isowner(input):
        input.conn.send("PRIVMSG "+input.conn.conf["owner"]+" :"+input.nick+" has asked wololo ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.") 

@hook.command
def ab(inp, input=None, bot=None):
    ".ab <botnick> <factoid> -- asks <botnick> <factoid>."
    if not inp == "":
        botn = inp.split(" ")
        botn = botn[0]
        input.conn.send("PRIVMSG "+botn+" :?" + inp + " > " + input.nick)  
    if not perm.isowner(input):     
        input.conn.send("PRIVMSG "+input.conn.conf["owner"]+" :"+input.nick+" has asked "+botn+" ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.")
		


@hook.command(owneronly=True)
def test(inp, input=None, bot=None):
    for channels in input.conn.conf["channels"]:
        input.conn.send("names "+channels)
          
@hook.command(owneronly=True)
def tests(inp, input=None, bot=None):
    list = dircache.listdir(bot.persist_dir)
    x=-1
    list2=[]
    print(list)
    for file in list:
        if str(file).endswith(".db"):
            x=x+1
            print(file+" "+str(x))
            list2.append(str(file))
    input.say(' '.join(list2))

@hook.command(owneronly=True)
def test2(inp, input=None, bot=None):
    input.say(' '.join(input.conn.users.channels))
