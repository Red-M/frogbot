#the plugin "awatch.py" written by Red-M on Github or Red_M on esper.net has been moved here.
import re
from util import hook, perm, munge

@hook.sieve
def sieve_suite(bot, input, func, kind, args):
    inuserhost = input.user+'@'+input.host
    ignored = input.conn.conf['ignore']
    if input.nick in input.conn.conf['owner'] and input.conn.conf['superadmins'].count(input.nick)==0 and input.conn.conf['admins'].count(input.nick)==0:
        input.conn.conf['superadmins'].append(input.nick)
        input.conn.conf['admins'].append(input.nick)
    if inuserhost in input.conn.conf['owner'] and input.conn.conf['superadmins'].count(inuserhost)==0 and input.conn.conf['admins'].count(inuserhost)==0:
        input.conn.conf['superadmins'].append(inuserhost)
        input.conn.conf['admins'].append(inuserhost)
    if input.nick in input.conn.conf['superadmins'] and input.conn.conf['admins'].count(input.nick)==0:
        input.conn.conf['admins'].append(input.nick)
    if inuserhost in input.conn.conf['superadmins'] and input.conn.conf['admins'].count(inuserhost)==0:
        input.conn.conf['admins'].append(inuserhost)

    if kind == "command":
        if input.trigger in bot.config["disabled_commands"]:
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


#the extended permissions were moved here.
    if args.get('adminonly', False):
        if not perm.isadmin(input):
            return None
    if args.get('superadminonly', False):
        if not perm.issuperadmin(input):
            return None
    if args.get('owneronly', False):
        if not perm.isowner(input):
            return None
#extended permissions end here.

    return input
