# written by Red-M on github or Red_M on irc.esper.net
from util import hook
import usertracking
import sys
import time
import re
import json
from util import perm

@hook.command("addadmin")
@hook.command
def aad(inp, bot=None, input=None):
	"adds a nick/host to the admin list..."
	if perm.issuperadmin(input) and bot.config["admins"].count(inp)==0:
		bot.config["admins"].append(inp)
		json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
		return"Done."
	else:
		return"already an admin..."

@hook.command("removeadmin")
@hook.command
def ard(inp, bot=None, input=None):
	"removes a nick/host from the admin list..."
	if perm.issuperadmin(input) and bot.config["admins"].count(inp)>=1:
		bot.config["admins"].remove(inp)
		json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
		return"Done."
	else:
		input.say("not an admin...")

@hook.command("addsuperadmin")
@hook.command
def asa(inp, bot=None, input=None):
	"adds a nick/host to the super amdin list..."
	if perm.isowner(input) and bot.config["superadmins"].count(inp)==0:
		bot.config["superadmins"].append(inp)
		json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
		return"Done."
	else:
		return"already a super admin..."

@hook.command("removesuperadmin")
@hook.command
def arsa(inp, bot=None, input=None):
	"removes a nick/host from the super amdin list..."
	if perm.isowner(input) and bot.config["superadmins"].count(inp)==1:
		bot.config["superadmins"].remove(inp)
		json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
		return"Done."
	else:
		return"not a super admin..."

@hook.command("checkvalue")
@hook.command
def cheval(inp, bot=None, input=None, nick=None, db=None, chan=None):
	"checks the bot for values. admins only..."
	if not perm.isadmin(input):
 		return "nope.avi"
	if input.inp_unstripped.startswith('conn.conf["nickserv_password"][') or input.inp_unstripped.startswith('input.conn.conf["nickserv_password"][') or input.inp_unstripped.startswith('bot.config["nickserv_password"][') or input.inp_unstripped.startswith("bot.config['nickserv_password'][") or input.inp_unstripped.startswith('input.bot.config["nickserv_password"][') or input.inp_unstripped.startswith('input.bot.conf.get') or input.inp_unstripped.startswith('input.conn.conf.get') or input.inp_unstripped.startswith('bot.config["nickserv_password"][') or input.inp_unstripped.startswith('bot.config.get("nickserv_password"'):
		input.conn.send("PRIVMSG "+str(bot.config['owner']).replace("u'","").replace("'","").replace("[","").replace("]","")+" :someone tried to steal your password but failed...")
		return "Nope.avi! fuck no. try that shit again and ill lop your head off!"
	inpss = "input.say(str("+inp+"))"
	try:
	
		_blah = dict(globals())
		_blah.update(input)
		_blah.update(locals())
		exec inpss in _blah
        	return _blah["_r"] if "_r" in _blah else None
	except:
		import traceback
		s = traceback.format_exc()
		sp = [x for x in s.split("\n") if x]
		if len(sp) > 2: sp = sp[-2:]
		for i in sp:
			input.notice(i)

@hook.command("stfu")
@hook.command
def ignore(inp, bot=None, input=None):
	"adds a nick/host to the ignore list..."
	if inp=='':
		input.say("no nick was added to ignore...ignoring command...")
	if perm.isadmin(input):
		if bot.config["ignore"]=='':
			bot.config["ignore"].append(inp)
			json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
			
		else:
			if bot.config["ignore"].count(inp)==0:
				bot.config["ignore"].append(inp)
				bot.config["ignore"].sort()
				json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
				input.say("done.")
			else:
				input.say("already ignored...")
	else:
		return"Nope.avi"

@hook.sieve
def ignoress(bot, input, func, kind, args):
	inuserhost = input.user+'@'+input.host
	if perm.isignored(input):
		return
	else:
		return input

@hook.command("kthx")
@hook.command
def listen(inp, bot=None, input=None):
	"removes the nick/host from the ignore list..."
	if inp=='':
		input.say("no nick was added to listen to...ignoring command...")
		return None
	if perm.isadmin(input):
		bot.config["ignore"].remove(inp)
		json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
		input.say("done.")
		return None
	else:
		return"Nope.avi"

@hook.command("pokerface")
@hook.command("ignorelist")
@hook.command
def ign(inp, bot=None, input=None):
	"lists the currently ignored people..."
	outrs=', '.join(input.bot.config["ignore"])
	if outrs=='':
		input.say("I am currently ignoring no one!")
	else:
		if inp=='':
			input.say("I am currently ignoring these people \x034,1"+outrs+".")
		else: 
			if input.bot.config["ignore"].count(inp)==1:
				input.say("I am ignoring this person...")
			else:
				input.say("I do not have that person on my ignore list...")