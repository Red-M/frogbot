# method from Lukeroge edited and adjusted for frog by Red-M on github
# or Red_M on esper.net

def isadmin(input):
	inuserhost=input.user+'@'+input.host
	if (input.nick in input.conn.conf["admins"] \
    or inuserhost in input.conn.conf["admins"] \
    or str(input.nick) in input.bot.auth[str(input.conn.server)]["admin"] \
    or str(input.nick) in input.bot.auth[str(input.conn.server)]["superadmin"] \
    or str(input.nick) in input.bot.auth[str(input.conn.server)]["owner"]):
		return True
	else:
		return False
def issuperadmin(input):
	inuserhost = input.user+'@'+input.host
	if input.nick in input.conn.conf["superadmins"] \
    or inuserhost in input.conn.conf["superadmins"] \
    or str(input.nick) in input.bot.auth[str(input.conn.server)]["superadmin"] \
    or str(input.nick) in input.bot.auth[str(input.conn.server)]["owner"]:
		return True
	else:
		return False
def isowner(input):
	inuserhost = input.user+'@'+input.host
	if (input.nick in input.conn.conf["owner"] \
    or inuserhost in input.conn.conf["owner"] \
    or str(input.nick) in input.bot.auth[str(input.conn.server)]["owner"]):
		return True
	else:
		return False
def isbot(input):
	inuserhost = input.user+'@'+input.host
	if input.nick in input.conn.conf["bots"] \
    or inuserhost in input.conn.conf["bots"]:
		return True
	else:
		return False
def isignored(input):
	inuserhost = input.user+'@'+input.host
	if ((input.nick in input.conn.conf["ignore"]) \
    or (inuserhost in input.conn.conf["ignore"]) \
    or (input.chan in input.conn.conf["ignore"])) \
    and input.nick not in input.conn.conf["admins"]:
		return True
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
            