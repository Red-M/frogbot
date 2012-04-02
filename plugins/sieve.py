import re

from util import hook
from util import perm

@hook.sieve
def sieve_suite(bot, input, func, kind, args):
    inuserhost = input.user+'@'+input.host
    ignored = bot.config["ignore"]
    if perm.isowner(input) and bot.config["superadmins"].count(input.nick)==0 and bot.config["admins"].count(input.nick)==0:
        bot.config["superadmins"].append(input.nick)
        bot.config["admins"].append(input.nick)
    if perm.isowner(input) and bot.config["superadmins"].count(inuserhost)==0 and bot.config["admins"].count(inuserhost)==0:
        bot.config["superadmins"].append(inuserhost)
        bot.config["admins"].append(inuserhost)
    if perm.issuperadmin(input) and bot.config["admins"].count(input.nick)==0:
        bot.config["admins"].append(input.nick)
    if perm.issuperadmin(input) and bot.config["admins"].count(inuserhost)==0:
        bot.config["admins"].append(inuserhost) 

    if kind == "command":
        if input.trigger in bot.config["disabled_commands"]:
            return None

    if perm.isignored(input) or perm.isbot(input):
        if not perm.isadmin(input):
            return None
    if type == "event" and perm.isignored(input):
        if not perm.isadmin(input):
            return None

    fn = re.match(r'^plugins.(.+).py$', func._filename)
    disabled = bot.config.get('disabled_plugins', [])
    if fn and fn.group(1).lower() in disabled:
        return None

    acl = bot.config.get('acls', {}).get(func.__name__)
    if acl:
        if 'deny-except' in acl:
            allowed_channels = map(unicode.lower, acl['deny-except'])
            if input.chan.lower() not in allowed_channels:
                return None
        if 'allow-except' in acl:
            denied_channels = map(unicode.lower, acl['allow-except'])
            if input.chan.lower() in denied_channels:
                return None

    if args.get('adminonly', False):
        if perm.isadmin(input):
            return None
    if args.get('superadminonly', False):
        if perm.issuperadmin(input):
            return None
    if args.get('owneronly', False):
        if perm.isowner(input):
            return None

    return input
