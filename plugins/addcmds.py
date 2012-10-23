# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook, perm
import os, sys, time, json, socket

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
            if inp=="":
                bot.conns[xcon].send('QUIT :\x02\x034,1Kill switch '
                                    'activated by %s.' % (input.nick))
            else:
                bot.conns[xcon].send('QUIT :\x02\x034,1Kill switch '
                        'activated by %s. Reason: %s' % (input.nick, inp))
        time.sleep(0.1)
        if os.name == 'posix':
            #client("127.0.0.1", 4329, "bot term. shutdown. NOW")
            os.system("kill "+str(os.getpid()))
        elif os.name == 'nt':
            #client("127.0.0.1", 4329, "bot term. shutdown. NOW")
            os.system("taskkill "+str(os.getpid()))

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
            if inp=="":
                bot.conns[xcon].send('QUIT :\x02\x034,1Restart switch '
                                    'activated by %s.' % (input.nick))
            else:
                bot.conns[xcon].send('QUIT :\x02\x034,1Restart switch '
                        'activated by %s. Reason: %s' % (input.nick, inp))
        time.sleep(0.1)
        if os.name == 'posix':
            client("127.0.0.1", 4329, "bot term. shutdown. NOW")
            time.sleep(1)
            pid = os.getpid()
            os.execl("./b", "b")
            os.system("kill %s" % (pid))
        elif os.name == 'nt':
            os.system(bot.config["restartcmd"])
            client("127.0.0.1", 4329, "bot term. shutdown. NOW")
            time.sleep(1)
            pid = os.getpid()
            os.system("taskkill /PID %s" % (pid))

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
    finally:
        sock.close()
            
#@hook.command    usertracking was removed so this became broken.... meh it was only a testing plugin
def users(inp, bot=None, input=None):
    if perm.isadmin(input):
        input.say(" ".join(input.conn.users.users))

@hook.command("channels")
@hook.command
def chan(inp, input=None, db=None, bot=None, users=None):
    "lists the current channels that I am in..."
    outrs='\x02, \x02'.join(input.conn.conf['channels'])
    input.conn.send("PRIVMSG %s :I am in these channels:"
                                " \x02%s." % (input.chan,outrs))

@hook.command
def raw(inp, input=None):
	"sends a raw irc command. bot owner only..."
	if perm.isowner(input):
		input.conn.send(inp)
	else:
		input.conn.send("PRIVMSG %s :You cannot do this." % (input.nick))
		
