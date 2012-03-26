# written by Red-M on github or Red_M on irc.esper.net
from util import hook
import usertracking
import sys
import time
import re

@hook.command
def aad(inp, bot=None, input=None):
	if input.nick in input.bot.config["superadmins"] and bot.config["admins"].count(inp)==0:
		bot.config["admins"].append(inp)
		return"Done."
	else:
		return"already an admin..."

@hook.command
def asa(inp, bot=None, input=None):
	if input.nick in input.bot.config["owner"] and bot.config["superadmins"].count(inp)==0:
		bot.config["superadmins"].append(inp)
		return"Done."
	else:
		return"already a super admin..."

@hook.command
def cheval(inp, bot=None, input=None, nick=None, db=None, chan=None):
	if not input.nick in bot.config["admins"]:
 		return "nope.avi"
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

@hook.command
def ignore(inp, bot=None, input=None):
	if inp=='':
		return"no nick was added to ignore...ignoring command..."
	if input.nick in input.bot.config["admins"]:
		if bot.config["ignore"]=='':
			bot.config["ignore"].append(inp)
			
		else:
			if bot.config["ignore"].count(inp)==0:
				bot.config["ignore"].append(inp)
				bot.config["ignore"].sort()
				return"done."
			else:
				return"already ignored..."
	else:
		return"Nope.avi"

@hook.sieve
def ignoress(bot, input, func, kind, args):
	if input.nick in bot.config["ignore"]:
		return
	else:
		return input

@hook.command
def listen(inp, bot=None, input=None):
	if inp=='':
		return"no nick was added to listen to...ignoring command..."
	if input.nick in input.bot.config["admins"]:
		bot.config["ignore"].remove(inp)
		return"done."
	else:
		return"Nope.avi"

@hook.command
def ign(inp, bot=None, input=None):
	outrs=str(input.bot.config["ignore"])
	outrs=outrs.replace("u'","")
	outrs=outrs.replace("'","")
	outrs=outrs.replace("[","")
	outrs=outrs.replace("]","")
	if outrs=='':
		return"I am currently ignoring no one!"
	else:
		if inp=='':
			return"I am currently ignoring these people "+outrs+"."
		else: 
			if input.bot.config["ignore"].count(inp)==1:
				return"I am ignoring this person..."
			else:
				return"I do not have that person on my ignore list..."