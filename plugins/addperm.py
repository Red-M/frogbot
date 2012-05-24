# written by Red-M on github or Red_M on irc.esper.net
from util import hook, perm, munge
import json

@hook.command("addadmin")
@hook.command
def aad(inp, bot=None, input=None):
	"adds a nick/host to the admin list..."
	if perm.issuperadmin(input) and input.conn.conf["admins"].count(inp)==0:
		input.conn.conf["admins"].append(inp)
		confofall=bot.config
		for xcon in bot.conns:
			confofall['connections'][xcon]=bot.conns[xcon].conf
		json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
		return"Done."
	else:
		return"already an admin..."

@hook.command("removeadmin")
@hook.command
def ard(inp, bot=None, input=None):
	"removes a nick/host from the admin list..."
	if perm.issuperadmin(input) and input.conn.conf["admins"].count(inp)>=1:
		input.conn.conf["admins"].remove(inp)
		confofall=bot.config
		for xcon in bot.conns:
			confofall['connections'][xcon]=bot.conns[xcon].conf
		json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
		return"Done."
	else:
		input.say("not an admin...")
		

@hook.command("addbot")
@hook.command
def aab(inp, bot=None, input=None):
	"adds a nick/host to the bots list..."
	if perm.isadmin(input) and input.conn.conf["bots"].count(inp)==0:
		input.conn.conf["bots"].append(inp)
		confofall=bot.config
		for xcon in bot.conns:
			confofall['connections'][xcon]=bot.conns[xcon].conf
		json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
		return"Done."
	else:
		return"already on bot list..."

@hook.command("removebot")
@hook.command
def arb(inp, bot=None, input=None):
	"removes a nick/host from the bots list..."
	if perm.isadmin(input) and input.conn.conf["bots"].count(inp)>=1:
		input.conn.conf["bots"].remove(inp)
		confofall=bot.config
		for xcon in bot.conns:
			confofall['connections'][xcon]=bot.conns[xcon].conf
		json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
		return"Done."
	else:
		input.say("not a bot...")


@hook.command("addsuperadmin")
@hook.command
def asa(inp, bot=None, input=None):
	"adds a nick/host to the super amdin list..."
	if perm.isowner(input) and input.conn.conf["superadmins"].count(inp)==0:
		input.conn.conf["superadmins"].append(inp)
		confofall=bot.config
		for xcon in bot.conns:
			confofall['connections'][xcon]=bot.conns[xcon].conf
		json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
		return"Done."
	else:
		return"already a super admin..."

@hook.command("removesuperadmin")
@hook.command
def arsa(inp, bot=None, input=None):
	"removes a nick/host from the super amdin list..."
	if perm.isowner(input) and input.conn.conf["superadmins"].count(inp)==1:
		input.conn.conf["superadmins"].remove(inp)
		confofall=bot.config
		for xcon in bot.conns:
			confofall['connections'][xcon]=bot.conns[xcon].conf
		json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
		return"Done."
	else:
		return"not a super admin..."

@hook.command("stfu")
@hook.command
def ignore(inp, bot=None, input=None):
	"adds a nick/host to the ignore list..."
	if inp=='':
		input.say("no nick was added to ignore...ignoring command...")
	if perm.isadmin(input):
		if input.conn.conf["ignore"].count(inp)==0:
			input.conn.conf["ignore"].append(inp)
			input.conn.conf["ignore"].sort()
			confofall=bot.config
			for xcon in bot.conns:
				confofall['connections'][xcon]=bot.conns[xcon].conf
			json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
			input.say("done.")
		else:
			return("already ignored...")
	else:
		return"Nope.avi"

@hook.sieve
def ignoress(bot, input, func, kind, args):
	if perm.isignored(input) or perm.isbot(input):
		if not perm.isadmin(input):
			return None
		else:
			return input
	else:
		return input

@hook.command("kthx")
@hook.command
def listen(inp, bot=None, input=None):
	"removes the nick/host from the ignore list..."
	if not perm.isadmin(input):
		return("Nope.avi")
	else:
		if perm.isadmin(input) and not inp=='':
			if input.conn.conf["ignore"].count(inp)==1:
				input.conn.conf["ignore"].remove(inp)
				confofall=bot.config
				for xcon in bot.conns:
					confofall['connections'][xcon]=bot.conns[xcon].conf
				json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
				return("done.")
			else:
				return "I am not ignoring that person at this time."
		else:
			return("invalid syntax. ,listen <channel or nick to be listened to>")

@hook.command("botlist")
@hook.command
def bol(inp, bot=None, input=None):
	"lists the currently ignored bots on the bot list..."
	outrs=', '.join(input.conn.conf["bots"])
	if outrs=='':
		input.say("I am currently ignoring not one single bot!")
	else:
		if inp=='':
			#input.say("I am currently ignoring these bots \x02\x034,1"+outrs+"\x02\x031,0.")
			input.say("I am currently ignoring these bots \x02"+outrs+"\x02.")
		else: 
			if input.conn.conf["bot"].count(inp)==1:
				input.say("I am ignoring this bot...")
			else:
				input.say("I do not have that bot on my bot list...")
		
@hook.command("pokerface")
@hook.command("ignorelist")
@hook.command
def ign(inp, bot=None, input=None):
	"lists the currently ignored people..."
	outrs=', '.join(input.conn.conf["ignore"])
	if outrs=='':
		input.say("I am currently ignoring no one!")
	else:
		if inp=='':
			#input.say("I am currently ignoring these people \x02\x034,1"+outrs+"\x02\x031,0.")
			input.say("I am currently ignoring these people \x02"+outrs+"\x02.")
		else: 
			if input.conn.conf["ignore"].count(inp)==1:
				input.say("I am ignoring this person...")
			else:
				input.say("I do not have that person on my ignore list...")

@hook.command("adm")
@hook.command
def admins(inp, bot=None, input=None):
	"tells the current admins of the bot..."
	outos=', '.join(input.conn.conf["admins"])
	outos=munge.muninput(input, bot, outos)
	input.conn.send("PRIVMSG "+ input.chan +" :The Admins of this bot are: \x02"+outos)
#	input.conn.send("PRIVMSG "+ input.chan +" :The Admins of this bot are: \x02\x034,1"+outos)

@hook.command("sadm")
@hook.command
def superadmins(inp, bot=None, input=None):
	"tells the current admins of the bot..."
	outos=', '.join(input.conn.conf["superadmins"])
	outos=munge.muninput(input, bot, outos)
	input.conn.send("PRIVMSG "+ input.chan +" :The Super Admins of this bot are: \x02"+outos)
#	input.conn.send("PRIVMSG "+ input.chan +" :The Admins of this bot are: \x02\x034,1"+outos)

@hook.command("own")
@hook.command
def owner(inp, bot=None, input=None):
	"tells the current admins of the bot..."
	outos=', '.join(input.conn.conf["owner"])
	outos=munge.muninput(input, bot, outos)
	input.conn.send("PRIVMSG "+ input.chan +" :The Owner of this bot is: \x02"+outos)
#	input.conn.send("PRIVMSG "+ input.chan +" :The Owner of this bot is: \x02\x034,1"+outos)

@hook.command
def gtfo(inp, input=None, bot=None):
    "makes me leave the channel. can be used by a channel op or bot admin..."
    if perm.isadmin(input) or "o" in input.conn.users[input.chan].usermodes[input.nick][0]:
        if input.conn.conf['channels'].count(inp)==1:
            input.conn.conf['channels'].remove(inp)
            confofall=bot.config
            for xcon in bot.conns:
                confofall['connections'][xcon]=bot.conns[xcon].conf
            json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
        input.conn.send("PART "+input.chan)
    else:
        input.conn.send("PRIVMSG "+input.nick+" :You cannot do this.")
		
