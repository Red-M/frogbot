# method from Lukeroge edited and adjusted for frog by Red-M on github
# or Red_M on esper.net
import re

def permcheck(input,type,type2):
    inuserhost = input.nick+'!'+input.user+'@'+input.host
    list=[]
    i=0
    for data in input.conn.conf[type]:
        regex = re.compile(data.replace("*",".*"))
        match = regex.search(inuserhost)
        i=i+1
        if (match and input.nick not in input.conn.conf[type2]) or str(input.nick) in input.bot.auth[str(input.conn.name)][type]):
            return True
        else:
            if not match and len(input.conn.conf[type])==i:
                return False

def isadmin(input):
    if permcheck(input,"admins","ignore") or permcheck(input,"superadmins","ignore") or isowner(input):
        return True
    else:
        return False

def issuperadmin(input):
    if permcheck(input,"superadmins","ignore") or isowner(input):
        return True
    else:
        return False

def isowner(input):
    inuserhost = input.user+'@'+input.host
    if (input.nick in input.conn.conf["owner"] \
    or inuserhost in input.conn.conf["owner"] \
    or str(input.nick) in input.bot.auth[str(input.conn.name)]["owner"]):
        return True
    else:
        return False

def isbot(input):
    return permcheck(input,"bots","admins")
    
def isvoiced(input):
    if permcheck(input,"voiced","ignore") or permcheck(input,"admins","ignore") or permcheck(input,"superadmins","ignore") or isowner(input):
        return True
    else:
        return False
                
def isignored(input):
    inuserhost = input.nick+'!'+input.user+'@'+input.host
    list=[]
    i=0
    for data in input.conn.conf["ignore"]:
        if (input.chan in input.conn.conf["ignore"]) and (input.nick not in input.conn.conf["admins"]):
            return True
        else:
            if input.nick not in input.conn.conf["admins"]:
                regex = re.compile(data.replace("*",".*"))
                match = regex.search(inuserhost)
                i=i+1
                if (match and input.nick not in input.conn.conf["admins"]) \
                or (input.chan in input.conn.conf["ignore"]):
                    return True
                else:
                    if not match and len(input.conn.conf["ignore"])==i:
                        return False
            else:
                return False
        
def amsg(input,msg):
    for xcon in input.bot.conns:
        for channels in input.conn.channels:
            if channels not in bot.conns[xcon].conf["ignore"]:
                bot.conns[xcon].send('PRIVMSG %s :%s' % (channels,msg))
                
def repamsg(input,msg):
    for xcon in input.bot.conns:
        channels = input.bot.conns[xcon].conf["reportchan"]
        if channels not in input.bot.conns[xcon].conf["ignore"]:
            input.bot.conns[xcon].send('PRIVMSG %s :%s' % (channels,msg))
            