# written by Red-M on github or Red_M on irc.esper.net
from util import hook

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
			if outrs.count(input.bot.config["ignore"]))==1:
				return"I am ignoring this person..."
			else:
				return"I do not have that person on my ignore list..."
		else:
			return"error..."