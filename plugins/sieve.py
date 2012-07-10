#the plugin "awatch.py" written by Red-M on Github or Red_M on esper.net has been moved here.
import re, time
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
        if "^" in input.paraml[1]:
            input.inp.replace("^",bot.chanseen[input.conn.server][input.chan][0])
            input.paraml[1].replace("^",bot.chanseen[input.conn.server][input.chan][0])
        if input.trigger in bot.config["disabled_commands"]:
            return None

    if input.paraml[0].startswith("\x01PING "):
		input.conn.send("NOTICE "+input.nick+" :"+input.inp[1])

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

    if kind=="event" and (perm.isignored(input) or perm.isbot(input)):
        if not perm.isadmin(input) and (not "NICK" in args["events"]):
            return None
        else:
            return input
    else:
        return input

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
    
def db_init(db):
    db.execute("create table if not exists seen(name, said, time, chan)")
    db.commit()
    
def seen_get(db, input):
    row = db.execute("select said from seen where name=(?)", (input.paraml[1].lower())).fetchone()
    time = db.execute("select time from seen where name=(?)", (input.paraml[1].lower())).fetchone()
    chan = db.execute("select chan from seen where name=(?)", (input.paraml[1].lower())).fetchone()
    if row:
        return paraml[1]+" said '"+row[0]+"' in "+chan[0]+" at "+time[0]
    else:
        return None
        
def seen_save(db, input):
    db.execute("delete from seen where name=(?)", (input.nick.lower(),)).rowcount
    db.execute("insert or replace into seen(name,said,time,chan) values(?,?,?,?)", (input.nick.lower(), input.paraml[1], time.time(), input.chan.lower()))
    db.commit()
    
@hook.singlethread
@hook.event('PRIVMSG')
def seen_user(inp, nick='', db_seen=None, input=None, bot=None):
    db_init(db_seen)
    seen_save(db_seen, input)
    
@hook.event('PRIVMSG')
def chanwatching(inp, input=None, bot=None):
    if not input.chan in bot.chanseen[input.conn.server]:
        bot.chanseen[input.conn.server][input.chan]=[]
        bot.chanseen[input.conn.server][input.chan].append(input.paraml[1])
    if len(bot.chanseen[input.conn.server][input.chan])==1:
        bot.chanseen[input.conn.server][input.chan].insert(1, bot.chanseen[input.conn.server][input.chan][0])
        time.sleep(.1)
        bot.chanseen[input.conn.server][input.chan].insert(0, input.paraml[1])
    bot.chanseen[input.conn.server][input.chan].insert(1, bot.chanseen[input.conn.server][input.chan][0])
    time.sleep(.1)
    bot.chanseen[input.conn.server][input.chan].insert(0, input.paraml[1])
    id = len(bot.chanseen[input.conn.server][input.chan])
    for idel in bot.chanseen[input.conn.server][input.chan]:
        if len(bot.chanseen[input.conn.server][input.chan])>=3:
            id = id-1
            bot.chanseen[input.conn.server][input.chan].pop(id)
    
@hook.event('PRIVMSG')
def userwatching(inp, nick='', chan='', input=None, bot=None):
    if not input.nick in bot.seen[input.conn.server]:
        bot.seen[input.conn.server][input.nick]=[]
        bot.seen[input.conn.server][input.nick].append(input.paraml[1])
    if len(bot.seen[input.conn.server][input.nick])==1:
        bot.seen[input.conn.server][input.nick].insert(1, bot.seen[input.conn.server][input.nick][0])
        time.sleep(.1)
        bot.seen[input.conn.server][input.nick].insert(0, input.paraml[1])
    bot.seen[input.conn.server][input.nick].insert(1, bot.seen[input.conn.server][input.nick][0])
    time.sleep(.1)
    bot.seen[input.conn.server][input.nick].insert(0, input.paraml[1])
    id = len(bot.seen[input.conn.server][input.nick])
    for idel in bot.seen[input.conn.server][input.nick]:
        if len(bot.seen[input.conn.server][input.nick])>=3:
            id = id-1
            bot.seen[input.conn.server][input.nick].pop(id)