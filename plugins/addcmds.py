# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook, perm
import os, sys, time, json

@hook.command
def kl(inp, say=None, nick=None, input=None, bot=None):
    "kill switch."
    if not perm.isowner(input):
        input.notice("Only the bot owner can use this command!")
    elif perm.isowner(input):
        confofall=bot.config
        for xcon in bot.conns:
            confofall['connections'][xcon]=bot.conns[xcon].conf
        json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
        time.sleep(0.1)
        for xcon in bot.conns:
            bot.conns[xcon].send("NICK "+input.conn.nick+"|offline")
        time.sleep(0.5)
        for xcon in bot.conns:
            bot.conns[xcon].send('QUIT :\x02\x034,1Kill switch activated by '+input.nick+'.')
        time.sleep(0.1)
        if os.name == 'posix':
            pid = os.getpid()
            os.system("kill "+str(pid))
        elif os.name == 'nt':
            sys.exit(0)

@hook.command
def rl(inp, say=None, input=None, bot=None):
    "restart switch."
    if not perm.isadmin(input):
        input.notice("Only bot admins can use this command!")
    elif perm.isadmin(input):
        confofall=bot.config
        for xcon in bot.conns:
            confofall['connections'][xcon]=bot.conns[xcon].conf
        json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
        time.sleep(0.1)
        for xcon in bot.conns:
            bot.conns[xcon].send('QUIT :\x02\x034,1Restart switch activated by '+input.nick+'.')
        time.sleep(0.1)
        if os.name == 'posix':
            os.system("screen python ./bot.py")
            time.sleep(1)
            pid = os.getpid()
            os.system("kill "+str(pid))
        elif os.name == 'nt':
            os.system(bot.config["restartcmd"])
            time.sleep(1)
            sys.exit()

@hook.command
def users(inp, bot=None, input=None):
    input.say(" ".join(input.conn.users.users))

@hook.command("channels")
@hook.command
def chan(inp, input=None, db=None, bot=None, users=None):
    "lists the current channels that I am in..."
    outrs='\x02, \x02'.join(input.conn.conf['channels'])
    input.conn.send("PRIVMSG "+ input.chan +" :I am in these channels: \x02"+outrs+".")
#    input.conn.send("PRIVMSG "+ input.chan +" :I am in these channels: \x02\x034,1"+outrs)

@hook.command
def raw(inp, input=None):
	"sends a raw irc command. bot owner only..."
	if perm.isowner(input):
		input.conn.send(inp)
	else:
		input.conn.send("PRIVMSG "+input.nick+" :You cannot do this.")
		
