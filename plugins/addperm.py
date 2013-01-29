# written by Red-M on github or Red_M on irc.esper.net
from util import hook, perm, munge
import json, re

errorMsg = ("error. unknown error or not a valid use for this command. "
        "proper use: ,perm <add/remove|list> "
        "<bot/voice/admin/superadmin|bots/voiced/admins/superadmins> "
        "[nick or host to add/remove from the voice/admin/superadmin/bot list] "
        "where things in <> are required and [] are optional depending on "
        "wether or not you are adding/removing or listing a group and "
        "where / is one of these and | is one or the other.")

@hook.command("perm")
@hook.command
def permissions(inp, input=None, bot=None):
    "adds or removes permissions... use ,permissions help"
    check = input.inp.split(" ")
    cmdlist = ["add","remove","list","help"]
    if len(check)>=1:
        check[0]=check[0].lower()
    if len(check)>=2:
        check[1]=check[1].lower()
    if len(check)==0:
        return("Try using ',perm help' before stuffing around with"
        " this command.")
    if check[0] in cmdlist:
        if check[0]=="list" and len(check)==2:
            listlist=["bots","voice","admins","superadmins","owner"]
            if check[1]=="bots":
                return listbots(bot,input)
            if check[1]=="voiced":
                return listvoiced(bot,input)
            if check[1]=="admins":
                return listadmins(bot,input)
            if check[1]=="superadmins":
                return listsuperadmins(bot,input)
            if check[1]=="owner":
                return listowner(bot,input)
            elif not (check[1] in listlist):
                return("error. unknown error or not a permissions group.")
        if len(check)==3:
            check[1]=check[1].lower()
            if perm.isadmin(input):
                if check[0]=="add" and check[1]=="bot" and input.conn.conf["bots"].count(check[2])==0:
                    return addperm(check[2],bot,input,"bot")
                if check[0]=="remove" and check[1]=="bot" and input.conn.conf["bots"].count(check[2])==1:
                    return removeperm(check[2],bot,input,"bots")
                if check[0]=="add" and check[1]=="voice" and input.conn.conf["voiced"].count(check[2])==0:
                    return addperm(check[2],bot,input,"voice")
                if check[0]=="remove" and check[1]=="voice" and input.conn.conf["voiced"].count(check[2])==1:
                    return removeperm(check[2],bot,input,"voiced")
                else:
                    if check[1]=="bot" and check[0]=="add":
                        return("error. unknown error or already a "+check[1])
                    if check[1]=="bot" and check[0]=="remove":
                        return("error. unknown error or not a "+check[1])
            if perm.issuperadmin(input):
                if check[0]=="add":
                    if check[1]=="admin" and input.conn.conf["admins"].count(check[2])==0:
                        return addperm(check[2],bot,input,"admin")
                    if check[1]=="voice" and input.conn.conf["voiced"].count(check[2])==0:
                        return addperm(check[2],bot,input,"voice")
                    if check[1]=="bot" and input.conn.conf["bots"].count(check[2])==0:
                        return addperm(check[2],bot,input,"bot")
                    elif (check[1]=="bot" or check[1]=="admin" or check[1]=="voiced"):
                        return("error. unknown error or already a "+check[1])
                if check[0]=="remove":
                    if check[1]=="admin" and input.conn.conf["admins"].count(check[2])==1:
                        return removeperm(check[2],bot,input,"admins")
                    if check[1]=="voice" and input.conn.conf["voiced"].count(check[2])==1:
                        return removeperm(check[2],bot,input,"voiced")
                    if check[1]=="bot" and input.conn.conf["bots"].count(check[2])==1:
                        return removeperm(check[2],bot,input,"bots")
                    elif (check[1]=="bot" or check[1]=="admin"):
                        return("error. unknown error or not a "+check[1])
            if perm.isowner(input):
                if check[0]=="add":
                    if check[1]=="admin" and input.conn.conf["admins"].count(check[2])==0:
                        return addperm(check[2], bot, input,"admin")
                    if check[1]=="voice" and input.conn.conf["voiced"].count(check[2])==0:
                        return addperm(check[2], bot, input,"voice")
                    if check[1]=="superadmin" and input.conn.conf["superadmins"].count(check[2])==0:
                        return addperm(check[2], bot, input,"superadmin")
                    if check[1]=="bot" and input.conn.conf["bots"].count(check[2])==0:
                        return addperm(check[2],bot,input,"bot")
                    elif (check[1]=="bot" or check[1]=="admin" or check[1]=="superadmin"):
                        return("error. unknown error or already a "+check[1])
                if check[0]=="remove" and perm.isowner(input):
                    if check[1]=="admin" and input.conn.conf["admins"].count(check[2])==1:
                        return removeperm(check[2],bot,input,"admins")
                    if check[1]=="voice" and input.conn.conf["voiced"].count(check[2])==1:
                        return removeperm(check[2],bot,input,"voiced")
                    if check[1]=="superadmin" and input.conn.conf["superadmins"].count(check[2])==1:
                        return removeperm(check[2],bot,input,"superadmins")
                    if check[1]=="bot" and input.conn.conf["bots"].count(check[2])==1:
                        return removeperm(check[2],bot,input,"bots")
                    elif (check[1]=="bot" or check[1]=="admin" or check[1]=="superadmin"):
                        return ("error. unknown error or not a "+check[1])
            elif not perm.isadmin(input):
                return("You are not an admin or not high enough in "
                "this bot's permission's system to do this.")
        if check[0]=="help":
            return errorMsg
        elif not ((check[0]=="list" and len(check)==2) or (len(check)==3)):
            return errorMsg
    elif not check[0] in cmdlist:
        return errorMsg

def removeperm(inp, bot, input, type):
    input.conn.conf[type].remove(inp)
    confofall=bot.config
    for xcon in bot.conns:
        confofall['connections'][xcon]=bot.conns[xcon].conf
    json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)
    return"Done."

def addperm(inp, bot, input, type):
    regex = re.compile("(.*)!(.*)@(.*)")
    match = regex.search(inp)
    if type=="bot":
        type2="bots"
    if type=="voice":
        type2="voiced"
    if type=="admin":
        type2="admins"
    if type=="superadmin":
        type2="superadmins"
    if (inp=='' or inp=="*!*@*") or (not match):
        return("no hostmask was added to the "+type+" list...ignoring command...")
    if perm.isadmin(input) and match and (not match.group(1)=="" and not match.group(2)=="" and not match.group(3)==""):
        if input.conn.conf[type2].count(inp)==0:
            input.conn.conf[type2].append(inp)
            input.conn.conf[type2].sort()
            confofall=bot.config
            for xcon in bot.conns:
                confofall['connections'][xcon]=bot.conns[xcon].conf
                json.dump(confofall, open('config', 'w'), sort_keys=True, 
                                                            indent=1)
                return("done.")
        else:
            return("already a "+type+"...")
    else:
        return("Nope.avi")

def listbots(bot, input):
    outrs=', '.join(input.conn.conf["bots"])
    if outrs=='':
        return("I am currently ignoring not one single bot!")
    else:
        return("I am currently ignoring these bots \x02%s\x02." % (outrs))

def listadmins(bot, input):
    outos=[]
    for nicks in input.conn.conf["admins"]:
        if nicks=="":
            empty = removeperm(nicks, bot, "voice")
            print("found empty entries in admins. removed them.")
        if not nicks=="":
            outos.append(munge.muninput(input, bot, nicks))
    outoss=', '.join(outos)
    return("The Admins of this bot are: \x02%s" % (outoss))

def listsuperadmins(bot, input):
    outos=[]
    for nicks in input.conn.conf["superadmins"]:
        if nicks=="":
            empty = removeperm(nicks, bot, "superadmin")
            print("found empty entries in superadmins. removed them.")
        if not nicks=="":
            outos.append(munge.muninput(input, bot, nicks))
    outoss=', '.join(outos)
    return("The Super Admins of this bot are: \x02%s" % (outoss))

def listowner(bot, input):
    outos=munge.muninput(input, bot, input.conn.conf["owner"])
    return("The Owner of this bot is: \x02%s" % (outos))

def listvoiced(bot, input):
    outos=[]
    for nicks in input.conn.conf["voiced"]:
        if nicks=="":
            empty = removeperm(nicks, bot, "voice")
            print("found empty entries in voiced. removed them.")
        if not nicks=="":
            outos.append(munge.muninput(input, bot, nicks))
    outoss=', '.join(outos)
    return("The voiced users of this bot are: \x02%s" % (outoss))

@hook.command("stfu")
@hook.command
def ignore(inp, bot=None, input=None):
    "adds a hostmask to the ignore list... eg ,ignore <nick>!<ident>@<host> -- * can be used as an all"
    if not inp.startswith("#"):
        regex = re.compile("(.*)!(.*)@(.*)")
        match = regex.search(inp)
        if (inp=='' or inp=="*!*@*") or (not match):
            return("no hostmask was added to ignore...ignoring command...")
        if perm.isadmin(input) and match and (not match.group(1)=="" and not match.group(2)=="" and not match.group(3)==""):
            if input.conn.conf["ignore"].count(inp)==0:
                input.conn.conf["ignore"].append(inp)
                input.conn.conf["ignore"].sort()
                confofall=bot.config
                for xcon in bot.conns:
                    confofall['connections'][xcon]=bot.conns[xcon].conf
                json.dump(confofall, open('config', 'w'), sort_keys=True, 
                                                            indent=1)
                return("done.")
            else:
                return("already ignored...")
        else:
            return("Nope.avi")
    if inp.startswith("#"):
        if inp=='':
            return("no hostmask was added to ignore...ignoring command...")
        if perm.isadmin(input):
            if input.conn.conf["ignore"].count(inp)==0:
                input.conn.conf["ignore"].append(inp)
                input.conn.conf["ignore"].sort()
                confofall=bot.config
                for xcon in bot.conns:
                    confofall['connections'][xcon]=bot.conns[xcon].conf
                json.dump(confofall, open('config', 'w'), sort_keys=True, 
                                                            indent=1)
                return("done.")
            else:
                return("already ignored...")
        else:
            return("Nope.avi")


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
                json.dump(confofall, open('config', 'w'), sort_keys=True, 
                                                                indent=1)
                return("done.")
            else:
                return "I am not ignoring that person at this time."
        else:
            return("invalid syntax. ,listen "
            "<channel or nick to be listened to>")

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
            input.say("I am currently ignoring these people "
                                                    "\x02%s\x02." % (outrs))
        else: 
            if input.conn.conf["ignore"].count(inp)==1:
                input.say("I am ignoring this person...")
            else:
                input.say("I do not have that person on my ignore list...")

#@hook.command
def gtfo(inp, input=None, bot=None):
    "makes me leave the channel. can be used by a channel op or bot admin..."
    if perm.isadmin(input) \
            or "o" in input.conn.users[input.chan].usermodes[input.nick][0]:
        if input.conn.conf['channels'].count(inp)==1:
            input.conn.conf['channels'].remove(inp)
            confofall=bot.config
            for xcon in bot.conns:
                confofall['connections'][xcon]=bot.conns[xcon].conf
            json.dump(confofall, open('config', 'w'), sort_keys=True, 
                                                                indent=1)
        input.conn.send("PART %s" % (input.chan))
    else:
        input.conn.send("PRIVMSG %s :You cannot do this." % (input.nick))
        
