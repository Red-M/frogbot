# method from Lukeroge edited and adjusted for frog by Red-M on github or Red_M on esper.net

def isadmin(input):
	inuserhost=input.user+'@'+input.host
	if input.nick in input.bot.config["admins"] or inuserhost in input.bot.config["admins"]:
		return True
	else:
		return False
def issuperadmin(input):
	inuserhost = input.user+'@'+input.host
	if input.nick in input.bot.config["superadmins"] or inuserhost in input.bot.config["superadmins"]:
		return True
	else:
		return False
def isowner(input):
	inuserhost = input.user+'@'+input.host
	if input.nick in input.bot.config["owner"] or inuserhost in input.bot.config["owner"]:
		return True
	else:
		return False