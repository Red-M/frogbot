from util import hook, perm
import thread, re, json

auth_userlock = thread.allocate_lock()
flag_re = re.compile(r"^([@~&%+]*)(.*)$")
groupscheck=["admin","superadmin","owner"]

def userigntrack(old,new,input,bot):
    if input.conn.conf["ignore"].count(old)==1:
        if input.conn.conf["ignore"].count(input.mask)==0:
            input.conn.conf["ignore"].append(input.mask)
        input.conn.conf["ignore"].remove(old)
        input.conn.conf["ignore"].append(new)
        input.conn.conf["ignore"].sort()
        confofall=bot.config
        for xcon in bot.conns:
            confofall['connections'][xcon]=bot.conns[xcon].conf
        json.dump(confofall, open('config', 'w'), sort_keys=True, indent=1)

def usernick(old,new,conn,bot):
    for groupcheck in groupscheck:
        if old in bot.auth[str(conn.server)][groupcheck]:
            bot.auth[str(conn.server)][groupcheck][str(new)]={}
            del bot.auth[str(conn.server)][groupcheck][str(old)]
            
def userquit(nick,conn,bot):
    for groupcheck in groupscheck:
        if nick in bot.auth[str(conn.server)][groupcheck]:
            del bot.auth[str(conn.server)][groupcheck][str(nick)]

@hook.event("JOIN KICK QUIT NICK")
@hook.singlethread
def auth_track(inp, command=None, input=None, users=None,bot=None, db_auth=None):
    if not auth_userlock.acquire(): raise Exception("Problem acquiring auth_userlock, probable thread crash. Abort.")
    try:
        if command == "NICK":
            if perm.isignored(input):
                userigntrack(input.nick, inp[0], input, bot)
            usernick(input.nick, inp[0], input.conn, bot)
        if command == "QUIT":
            userquit(input.nick, input.conn, bot)
    except:
        raise
    finally:
        auth_userlock.release()