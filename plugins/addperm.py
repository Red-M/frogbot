# written by Red-M on github or Red_M on irc.esper.net
from util import hook, perm, munge
import json

@hook.command("perm")
@hook.command
def permissions(inp, input=None, bot=None):
	check = input.inp.split(" ")
	cmdlist = ["add","remove","list","help"]
	if len(check)>=1:
		check[0]=check[0].lower()
	if len(check)>=2:
		check[1]=check[1].lower()
	if len(check)==0:
		return("Try using ',perm help' before stuffing around with this command.")
	if check[0] in cmdlist:
		if check[0]=="list" and len(check)==2:
			listlist=["bot","admins","superadmins","owner"]
			if check[1]=="bots":
				rep = listbots(bot,input)
			if check[1]=="admins":
				rep = listadmins(bot,input)
			if check[1]=="superadmins":
				rep = listsuperadmins(bot,input)
			if check[1]=="owner":
				rep = listowner(bot,input)
			elif not (check[1] in listlist):
				rep = ("error. unknown error or not a permissions group.")
		if len(check)==3:
			check[1]=check[1].lower()
			if perm.isadmin(input):
				if check[0]=="add" and check[1]=="bot" and input.conn.conf["bots"].count(check[2])==0:
					rep = addbot(check[2],bot,input)
				if check[0]=="remove" and check[1]=="bot" and input.conn.conf["bots"].count(check[2])==1:
					rep = removebot(check[2],bot,input)
			if perm.issuperadmin(input):
				if check[0]=="add":
					if check[1]=="admin" and input.conn.conf["admins"].count(check[2])==0:
						rep = addadmin(check[2], bot, input)
					if check[1]=="bot" and input.conn.conf["bots"].count(check[2])==0:
						rep = addbot(check[2],bot,input)
					elif check[1]=="bot" or check[1]=="admin":
						rep = ("error. unknown error or already a "+check[1])
				if check[0]=="remove":
					if check[1]=="admin" and input.conn.conf["admins"].count(check[2])==1:
						rep = removeadmin(check[2],bot,input)
					if check[1]=="bot" and input.conn.conf["bots"].count(check[2])==1:
						rep = removebot(check[2],bot,input)
					elif check[1]=="bot" or check[1]=="admin":
						rep = ("error. unknown error or not a "+check[1])
			if perm.isowner(input):
				if check[0]=="add":
					if check[1]=="admin" and input.conn.conf["admins"].count(check[2])==0:
						rep = addadmin(check[2], bot, input)
					if check[1]=="superadmin" and input.conn.conf["superadmins"].count(check[2])==0:
						rep = addsuperadmin(check[2], bot, input)
					if check[1]=="bot" and input.conn.conf["bots"].count(check[2])==0:
						rep = addbot(check[2],bot,input)
					elif check[1]=="bot" or check[1]=="admin":
						rep = ("error. unknown error or already a "+check[1])
				if check[0]=="remove" and perm.isowner(input):
					if check[1]=="admin" and input.conn.conf["admins"].count(check[2])==1:
						rep = removeadmin(check[2],bot,input)
					if check[1]=="superadmin" and input.conn.conf["superadmins"].count(check[2])==1:
						rep = removesuperadmin(check[2],bot,input)
					if check[1]=="bot" and input.conn.conf["bots"].count(check[2])==1:
						rep = removebot(check[2],bot,input)
					elif check[1]=="bot" or check[1]=="admin":
						rep = ("error. unknown error or not a "+check[1])
			elif not perm.isadmin(input):
				rep = ("You are not an admin or not high enough in this bot's permission's system to do this.")
		if check[0]=="help":
			rep = ""
			input.conn.send("PRIVMSG "+input.nick+" :Proper use of ,perm is: ,perm <add/remove|list> <bot/admin/superadmin|bots/admins/superadmins> [nick or host to add/remove from the admin/superadmin/bot list] where things in <> are required and [] are optional depending on the wether or not you are adding/removing or listing a group and where / is one of these and | is one or the other.")
		elif not ((check[0]=="list" and len(check)==2) or (len(check)==3)):
			input.conn.send("error. unknown error or not a valid use for this command. proper use: ,perm <add/remove|list> <bot/admin/superadmin|bots/admins/superadmins> [nick or host to add/remove from the admin/superadmin/bot list] where things in <> are required and [] are optional depending on the wether or not you are adding/removing or listing a group and where / is one of these and | is one or the other.")
			rep = ""
	elif not check[0] in cmdlist:
		rep = "" 
		input.conn.send("error. unknown error or not a valid use for this command. proper use: ,perm <add/remove|list> <bot/admin/superadmin|bots/admins/superadmins> [nick or host to add/remove from the admin/superadmin/bot list] where things in <> are required and [] are optional depending on the wether or not you are adding/removing or listing a group and where / is one of these and | is one or the other.")
	return rep
		
def addadmin(inp, bot, input):
	input.conn.conf["admins"].append(inp)
	confofall=bot.config
	for xcon in bot.conns:
		confofall['connections'][xcon]=bot.conns[xcon].conf
	json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
	return"Done."

def removeadmin(inp, bot, input):
	input.conn.conf["admins"].remove(inp)
	confofall=bot.config
	for xcon in bot.conns:
		confofall['connections'][xcon]=bot.conns[xcon].conf
	json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
	return"Done."

def addbot(inp, bot, input):
	input.conn.conf["bots"].append(inp)
	confofall=bot.config
	for xcon in bot.conns:
		confofall['connections'][xcon]=bot.conns[xcon].conf
	json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
	return"Done."

def removebot(inp, bot, input):
	input.conn.conf["bots"].remove(inp)
	confofall=bot.config
	for xcon in bot.conns:
		confofall['connections'][xcon]=bot.conns[xcon].conf
	json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
	return"Done."

def addsuperadmin(inp, bot, input):
	input.conn.conf["superadmins"].append(inp)
	confofall=bot.config
	for xcon in bot.conns:
		confofall['connections'][xcon]=bot.conns[xcon].conf
	json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
	return"Done."

def removesuperadmin(inp, bot, input):
	input.conn.conf["superadmins"].remove(inp)
	confofall=bot.config
	for xcon in bot.conns:
		confofall['connections'][xcon]=bot.conns[xcon].conf
	json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
	return"Done."

def listbots(bot, input):
	outrs=', '.join(input.conn.conf["bots"])
	if outrs=='':
		return("I am currently ignoring not one single bot!")
	else:
		return("I am currently ignoring these bots \x02"+outrs+"\x02.")

def listadmins(bot, input):
	outos=', '.join(input.conn.conf["admins"])
	outos=munge.muninput(input, bot, outos)
	return("The Admins of this bot are: \x02"+outos)
#	input.conn.send("PRIVMSG "+ input.chan +" :The Admins of this bot are: \x02\x034,1"+outos)

def listsuperadmins(bot, input):
	outos=', '.join(input.conn.conf["superadmins"])
	outos=munge.muninput(input, bot, outos)
	return("The Super Admins of this bot are: \x02"+outos)
#	input.conn.send("PRIVMSG "+ input.chan +" :The Admins of this bot are: \x02\x034,1"+outos)

def listowner(bot, input):
	outos=', '.join(input.conn.conf["owner"])
	outos=munge.muninput(input, bot, outos)
	return("The Owner of this bot is: \x02"+outos)
#	input.conn.send("PRIVMSG "+ input.chan +" :The Owner of this bot is: \x02\x034,1"+outos)

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
		
