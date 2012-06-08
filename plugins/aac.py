# written by Red-M on github or Red_M on irc.esper.net
from util import hook, perm, http
import json, time

@hook.command
def save(inp, bot=None, input=None):
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
			inp = str(inp).replace("^", bot.chanseen[input.conn.server][input.chan][0])
		inpss= "input.say(str("+inp+"))"
		blocked=["sys.stdout",".connect()",'send("quit',"send('quit",'conn.connect()',"bot.conns[",'conf["ftp_pw"]','config["censored_strings"]','conf["server_password"]','conf["nickserv_password"]',"conf['ftp_pw']","config['censored_strings']","conf['server_password']","conf['nickserv_password']"]
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
			conn.msg(nickserv_name, nickserv_command2 % (conn.nick,nickserv_password))
			conn.msg(nickserv_name, nickserv_command % nickserv_password)
			time.sleep(1)
			bot.config['censored_strings'].append(nickserv_password)
			input.say("Done.")
	else:
		input.say("Nope.avi")
