# -*- coding: utf-8 -*-
from util import hook

character_replacements = {
    'a': 'ä',
    'b': 'Б',
    'c': 'ċ',
    'd': 'đ',
    'e': 'ë',
    'f': 'ƒ',
    'g': 'ġ',
    'h': 'ħ',
    'i': 'í',
    'j': 'ĵ',
    'k': 'ķ',
    'l': 'ĺ',
    'm': 'ṁ',
    'n': 'ñ',
    'o': 'ö',
    'p': 'ρ',
    'q': 'ʠ',
    'r': 'ŗ',
    's': 'š',
    't': 'ţ',
    'u': 'ü',
    'v': '',
    'w': 'ω',
    'x': 'χ',
    'y': 'ÿ',
    'z': 'ź',
    'A': 'Å',
    'B': 'Β',
    'C': 'Ç',
    'D': 'Ď',
    'E': 'Ē',
    'F': 'Ḟ',
    'G': 'Ġ',
    'H': 'Ħ',
    'I': 'Í',
    'J': 'Ĵ',
    'K': 'Ķ',
    'L': 'Ĺ',
    'M': 'Μ',
    'N': 'Ν',
    'O': 'Ö',
    'P': 'Р',
    'Q': 'Ｑ',
    'R': 'Ŗ',
    'S': 'Š',
    'T': 'Ţ',
    'U': 'Ů',
    'V': 'Ṿ',
    'W': 'Ŵ',
    'X': 'Χ',
    'Y': 'Ỳ',
    'Z': 'Ż'}

@hook.event("PRIVMSG")
def watch(inp, munge_count=0, command=None, input=None, bot=None, users=None):
	ignorenick = "Red_M" #nick to ignore within the quotes
	repchan = bot.config["reportchan"] #the channel to report back to
	cmdpre = "," #your cmd prefix
	reps = 0
	rep = ""
	nickf = input.nick
	for n in xrange(len(nickf)):
		rep = character_replacements.get(nickf[n])
		if rep:
			nickf = nickf[:n] + rep.decode('utf-8') + nickf[n + 1:]
			reps = reps + 1
			if reps == munge_count:
				break
	nickf = nickf
	cmduse = str(' '.join(sorted(bot.commands)))
	if input.inp[1].startswith(cmdpre):
		input.inp[1] = input.inp[1].replace(cmdpre,"")
		if input.inp[1]=="stfu":
			input.conn.send("PRIVMSG "+repchan+" :I have been muted in "+input.chan+" by "+nickf)
		if input.inp[1]=="kthx":
			input.conn.send("PRIVMSG "+repchan+" :I have been unmuted in "+input.chan+" by "+nickf)
		if input.inp[1]=="join":
			input.conn.send("PRIVMSG "+repchan+" :I have joined "+input.chan+" as told to by "+nickf)
		if input.inp[1]=="part":
			input.conn.send("PRIVMSG "+repchan+" :I have left "+input.chan+" as told to by "+nickf)
		if input.inp[1]=="gtfo":
			input.conn.send("PRIVMSG "+repchan+" :I have left "+input.chan+" as told to by "+nickf)
		if input.chan==input.nick and not input.nick==ignorenick and input.inp[1] in cmduse:
			input.conn.send("PRIVMSG "+repchan+" :"+nickf+" (used/try to use) ,"+input.inp[1]+" in a private message.")
		if input.chan.startswith("#") and not input.nick==ignorenick and input.inp[1] in cmduse:
			input.conn.send("PRIVMSG "+repchan+" :"+nickf+" (used/try to use) ,"+input.inp[1]+" in "+input.chan)
		if input.chan==repchan and not input.nick==ignorenick and input.inp[1] in cmduse:
			input.conn.send("PRIVMSG "+ignorenick+" :"+input.nick+" (used/try to use) ,"+input.inp[1]+" in "+repchan)
	elif input.inp[1].startswith("?") or input.inp[1].startswith("!") or (input.command=="PRIVMSG" and input.inp[1] in cmduse):
		if input.chan==input.nick and not input.nick==ignorenick:
			input.conn.send("PRIVMSG "+repchan+" :"+nickf+" asked me "+input.inp[1]+" in a private message.")
		else:
			if input.inp[1].startswith("?") and not input.nick==ignorenick:
				input.conn.send("PRIVMSG "+repchan+" :"+nickf+" asked me "+input.inp[1]+" in "+input.chan)
			if input.chan==repchan and not input.nick==ignorenick:
				input.conn.send("PRIVMSG "+ignorenick+" :"+input.nick+" said "+input.inp[1]+" in "+repchan)
