from util import hook
import thread, re

auth_userlock = thread.allocate_lock()
flag_re = re.compile(r"^([@~&%+]*)(.*)$")
groupscheck=["admin","superadmin","owner"]

def usernick(old,new,conn,bot):
    for groupcheck in groupscheck:
        if old in bot.auth[str(conn.server)][groupcheck]:
            bot.auth[str(conn.server)][groupcheck][str(new)]={}
            del bot.auth[str(conn.server)][groupcheck][str(old)]
            
def userquit(nick,conn,bot):
    for groupcheck in groupscheck:
        if nick in bot.auth[str(conn.server)][groupcheck]:
            del bot.auth[str(conn.server)][groupcheck][str(nick)]

@hook.event("JOIN KICK QUIT PRIVMSG MODE NICK")
@hook.singlethread
def auth_track(inp, command=None, input=None, users=None,bot=None, db_auth=None):
    if not auth_userlock.acquire(): raise Exception("Problem acquiring auth_userlock, probable thread crash. Abort.")
    try:
        if command == "NICK":
            usernick(input.nick, inp[0], input.conn, bot)
        if command == "QUIT":
            userquit(input.nick, input.conn, bot)
    except:
        raise
    finally:
        auth_userlock.release()