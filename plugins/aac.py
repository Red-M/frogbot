# written by Red-M on github or Red_M on irc.esper.net
from util import hook, perm, http
import json, time, re

@hook.command
def save(inp, bot=None, input=None):
	"saves the bot's config. bot admins only."
	if perm.isadmin(input):
		confofall=bot.config
		for xcon in bot.conns:
			confofall['connections'][xcon]=bot.conns[xcon].conf
		json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
		return "Done."
	else:
		return "Nope.avi"
		
def runcode(code,glo):
	return eval(code,glo)

@hook.command("checkvalue")
@hook.command
def cheval(inp, bot=None, input=None, nick=None, db=None, chan=None):
	"checks the bot for values. admins only..."
	if not perm.isadmin(input):
		return "Nope.avi"
	try:
		if '^' in input.paraml[1]:
			inp = str(inp).replace("^", \
                            bot.chanseen[input.conn.server][input.chan][0])
		inpss = "input.say(str("+inp+"))"
		blocked = ["sys.stdout",".connect",'.send',
        "bot.conns[",".conf",".config",".clear",".kill",
        "/home/redm","__import__"]
		igncmds=blocked
		for data in igncmds:
			if str(data) in input.inp:
				return "Nope.avi"
		_blah = dict(globals())
		_blah.update(input)
		runcode(inpss, _blah)
		if "_r" in _blah:
			out = _blah["_r"]
			igncmds=blocked
			for data in igncmds:
				if str(data) in input.inp:
					return "Nope.avi"
	except:
		import traceback
		s = traceback.format_exc()
		sp = [x for x in s.split("\n") if x]
		if len(sp) > 2: sp = sp[-2:]
		p=0
		for i in sp:
			p=p+1
			if p==1 and "^" in i:
				input.notice(i.replace(" ","_"))
			else:
				input.notice(i)
	
@hook.command
def ident(paraml, conn=None, bot=None, input=None):
	",ident   makes the bot identify with what ever..." \
    " use in case of fire or auto identify failing..."
	if perm.isadmin(input):
		nickserv_password = conn.conf.get('nickserv_password', '')
		nickserv_name = conn.conf.get('nickserv_name', 'nickserv')
		nickserv_command = conn.conf.get('nickserv_command', 'IDENTIFY %s')
		nickserv_command2 = conn.conf.get('nickserv_command', 'REGAIN %s %s')
		if nickserv_password:
			if nickserv_password in bot.config['censored_strings']:
				for x in range(0,bot.config['censored_strings'].count("^^")):
					bot.config['censored_strings'].remove("^^")
					bot.config['censored_strings'].remove("^^")
					bot.config['censored_strings'].remove(nickserv_password)
			conn.msg(nickserv_name, nickserv_command2 % (conn.nick,
                                                        nickserv_password))
			conn.msg(nickserv_name, nickserv_command % nickserv_password)
			time.sleep(1)
			bot.config['censored_strings'].append(nickserv_password)
			input.say("Done.")
	else:
		input.say("Nope.avi")

@hook.command        
def match(inp,input=None):
    inuserhost = input.nick+'!'+input.user+'@'+input.host
    list=[]
    i=0
    for data in input.conn.conf["ignore"]:
        regex = re.compile(data.replace("*",".*"))
        match = regex.search(inuserhost)
        i=i+1
        if (match and input.nick not in input.conn.conf["admins"]) \
        or (input.chan in input.conn.conf["ignore"]):
            return True
        else:
            if not match and len(input.conn.conf["ignore"])==i:
                return False