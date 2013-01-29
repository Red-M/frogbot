#the plugin "awatch.py" written by Red-M on Github or Red_M on esper.net has been moved here.
import re, time
from util import hook, perm, munge

@hook.sieve
def sieve_suite(bot, input, func, kind, args):
    inuserhost = input.user+'@'+input.host
    
    if perm.isignored(input) and not (perm.isvoiced(input)):
        if not (input.paraml[0].startswith("\x01ACTION ")):
            return None
        else:
            return input
    
    if perm.isbot(input):
        if not (input.paraml[0].startswith("\x01ACTION ")):
            return None
        else:
            return input

    if (input.chan in input.conn.conf["ignore"]) and not (perm.isvoiced(input)):
        if not (input.paraml[0].startswith("\x01ACTION ")):
            return None
        else:
            return input
            
    ignored = input.conn.conf['ignore']
    if kind == "command":
        if "^" in input.paraml[1]:
            input.inp = input.inp.replace("^",bot.chanseen[input.conn.name][input.chan][0])
            input.paraml[1] = input.paraml[1].replace("^",bot.chanseen[input.conn.name][input.chan][0])
        if input.trigger in bot.config["disabled_commands"]:
            return None
    
    connitem = input.conn
    for xconn in bot.conns:
        if connitem==bot.conns[xconn]:
            server=bot.conns[xconn].name
    if input.nick in bot.cooldown[str(server)]:
        bot.cooldown[str(server)][input.nick]+=1
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
    
@hook.event('PRIVMSG')
def cmdcooldown(inp,input=None,bot=None):
    wait=False
    connitem = input.conn
    for xconn in bot.conns:
        if connitem==bot.conns[xconn]:
            server=xconn
    if input.nick in bot.cooldown[str(server)]:
        bot.cooldown[str(server)][input.nick]+=20
    if ((not perm.isadmin(input)) and (not input.nick in bot.cooldown[str(server)]) and (not input.nick=="") and (input.inp[1].startswith(",") or input.inp[1].startswith("?") or input.inp[1].startswith("!")) and (not input.nick==input.conn.conf["nick"])):
        bot.cooldown[str(server)][input.nick]=7
        time.sleep(1)
        wait=True
    while wait==True:
        if bot.cooldown[str(server)][input.nick]<1:
            del bot.cooldown[str(server)][input.nick]
            wait=False
        else:
            bot.cooldown[str(server)][input.nick]+=-1
            time.sleep(1)
    
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
def seen_user(inp, nick='', db=None, input=None, bot=None):
    db_init(db)
    seen_save(db, input)
    
@hook.event('PRIVMSG')
def chanwatching(inp, input=None, bot=None):
    if not input.chan in bot.chanseen[input.conn.name]:
        bot.chanseen[input.conn.name][input.chan]=[]
        bot.chanseen[input.conn.name][input.chan].append(input.paraml[1])
    if len(bot.chanseen[input.conn.name][input.chan])==1:
        bot.chanseen[input.conn.name][input.chan].insert(1, bot.chanseen[input.conn.name][input.chan][0])
        time.sleep(.1)
        bot.chanseen[input.conn.name][input.chan].insert(0, input.paraml[1])
    bot.chanseen[input.conn.name][input.chan].insert(1, bot.chanseen[input.conn.name][input.chan][0])
    time.sleep(.1)
    bot.chanseen[input.conn.name][input.chan].insert(0, input.paraml[1])
    id = len(bot.chanseen[input.conn.name][input.chan])
    for idel in bot.chanseen[input.conn.name][input.chan]:
        if len(bot.chanseen[input.conn.name][input.chan])>=3:
            id = id-1
            bot.chanseen[input.conn.name][input.chan].pop(id)
    
@hook.event('PRIVMSG')
def userwatching(inp, nick='', chan='', input=None, bot=None):
    if not input.nick in bot.seen[input.conn.name]:
        bot.seen[input.conn.name][input.nick]=[]
        bot.seen[input.conn.name][input.nick].append(input.paraml[1])
    if len(bot.seen[input.conn.name][input.nick])==1:
        bot.seen[input.conn.name][input.nick].insert(1, bot.seen[input.conn.name][input.nick][0])
        time.sleep(.1)
        bot.seen[input.conn.name][input.nick].insert(0, input.paraml[1])
    bot.seen[input.conn.name][input.nick].insert(1, bot.seen[input.conn.name][input.nick][0])
    time.sleep(.1)
    bot.seen[input.conn.name][input.nick].insert(0, input.paraml[1])
    id = len(bot.seen[input.conn.name][input.nick])
    for idel in bot.seen[input.conn.name][input.nick]:
        if len(bot.seen[input.conn.name][input.nick])>=3:
            id = id-1
            bot.seen[input.conn.name][input.nick].pop(id)
