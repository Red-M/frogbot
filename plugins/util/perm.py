# method from Lukeroge edited and adjusted for frog by Red-M on github
# or Red_M on esper.net
import re

def permcheck(input,type,type2):
    inuserhost = input.nick+'!'+input.user+'@'+input.host
    list=[]
    i=0
    if type=="admins":
        type3="admin"
    if type=="superadmins":
        type3="superadmin"
    if not (type=="admins" or type=="superadmins"):
        type3=type
    for data in input.conn.conf[type]:
        data = data.replace("*",".*").replace("[","\\[").replace("]","\\]")
        regex = re.compile(data)
        match = regex.search(inuserhost)
        i=i+1
        if (((match) and (input.nick not in input.conn.conf[type2])) or (str(input.nick) in input.bot.auth[str(input.conn.name)][type3])):
            return True
        else:
            if not match and len(input.conn.conf[type])==i:
                return False
              
def permcheck2(input,type,type2):
    inuserhost = input.nick+'!'+input.user+'@'+input.host
    list=[]
    i=0
    for data in input.conn.conf[type]:
        regex = re.compile(data.replace("*",".+?"))
        match = regex.search(inuserhost)
        i=i+1
        if ((match) and (input.nick not in input.conn.conf[type2])):
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
    return permcheck2(input,"ignore","admins")
        
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
            