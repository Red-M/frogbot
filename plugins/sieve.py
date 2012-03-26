import re

from util import hook


@hook.sieve
def sieve_suite(bot, input, func, kind, args):
    inuserhost = input.user+'@'+input.host
    if input.nick in bot.config["owner"] and bot.config["superadmins"].count(input.nick)==0 and bot.config["admins"].count(input.nick)==0:
        bot.config["superadmins"].append(input.nick)
        bot.config["superadmins"].append(inuserhost)
        bot.config["admins"].append(input.nick)
        bot.config["admins"].append(inuserhost)
    if input.nick in bot.config["superadmins"] and bot.config["admins"].count(input.nick)==0:
        bot.config["admins"].append(input.nick)
        bot.config["admins"].append(inuserhost) 

    if kind == "command":
        if input.trigger in bot.config.get('disabled_commands', []):
            return None

        if type == "event":
            return input
        ignored = bot.config["ignore"]
        inuserhost = input.user+'@'+input.host
        if inuserhost in ignored or input.nick in ignored or input.chan in ignored and not (input.nick in bot.config["admins"] or input.nick in bot.config["superadmins"] or input.nick in bot.config["owner"] or inuserhost in bot.config["admins"] or inuserhost in bot.config["superadmins"] or inuserhost in bot.config["owner"]):
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
        admins = bot.config["admins"]
        inuserhost = input.user+'@'+input.host
        if inuserhost not in admins and input.nick not in admins:
            return None
    if args.get('sadminonly', False):
        sadmins=bot.config["superadmins"]
        inuserhost = input.user+'@'+input.host
        if inuserhost not in sadmins and input.nick not in sadmins:
            return None
    if args.get('owneronly', False):
        owner=bot.config["owner"]
        inuserhost = input.user+'@'+input.host
        if inuserhost not in owner and input.nick not in owner:
            return None

    return input
