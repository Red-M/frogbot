# authentication plugin written by Red-M on github or Red_M on esper.net
from util import hook, perm
import hashlib, thread, re, json


@hook.command('auth')
@hook.command
def authenticate(inp, input=None, db_global=None, bot=None, conn=None):
    "authenticate with this bot. NOTE: no password is stored in plain text. all passwords are stored as a sha512 hash. usage: ,auth login <username> <password>"
    db_global.execute("create table if not exists auth(user, pass, groups)")
    db_global.commit()
    check=input.inp.split(' ')
    #print(check)
    if len(check)==1 and check[0]=="help":
        out="To register with "+conn.nick+" please use ,auth <signup/reg> <username-you-want> <password-you-want>"
        out=out+". To login with "+conn.nick+" please use ,auth login <username-you-set> <password-you-set>"
        out=out+". If you forgot your password please contact "+conn.conf["owner"]+" about it."
        out=out+". For bot owners to change a user's group use ,auth groupset <username-of-person> <admin/superadmin/owner>"
        return(out)
    if len(check)==2 and check[0]=="logout":
        groupcheck=''.join(str(db_global.execute("select groups from auth where user=(?)",(check[1],)).fetchone()[0]))
        if input.nick in bot.auth[str(conn.name)][groupcheck]:
            del bot.auth[str(conn.name)][groupcheck][str(input.nick)]
            return "Bye!"
    if len(check)>=3:
        cmdlist=["login",'groupset','set','reset']
        if check[0] in cmdlist:
            usercheck=''.join(str(db_global.execute("select user from auth where user=(?)",(check[1],)).fetchone()[0]))
            passcheck=''.join(str(db_global.execute("select pass from auth where user=(?)",(check[1],)).fetchone()[0]))
            groupcheck=''.join(str(db_global.execute("select groups from auth where user=(?)",(check[1],)).fetchone()[0]))
        #print(usercheck+"\n"+passcheck+'\n'+groupcheck)
        if check[0]=='reg' or check[0]=='signup':
            usercheck=''.join(str(db_global.execute("select user from auth where user=(?)",(check[1],)).fetchone()))
            passcheck=''.join(str(db_global.execute("select pass from auth where user=(?)",(check[1],)).fetchone()))
            groupcheck=''.join(str(db_global.execute("select groups from auth where user=(?)",(check[1],)).fetchone()))
            check[2]=hashlib.sha512(check[2]).hexdigest()
            if check[1]==str(usercheck):
                return("you are already registered on this bot or choose another name.")
            else:
                db_global.execute("insert into auth(user, pass, groups) values (?,?,?)",(check[1], check[2],"none"))
                db_global.commit()
                perm.repamsg(input,input.nick+" is registering with me.")
                return("done. please login by using ,auth login "+check[1]+" <password-here>.")
        if check[0]=="login":
            print(input.nick+" is trying to auth as "+check[1])
            hashcheck=hashlib.sha512(check[2]).hexdigest()
            if usercheck==check[1] and passcheck==hashcheck:
                print(groupcheck)#if groupcheck==None
                bot.auth[str(conn.name)][groupcheck][str(input.nick)]={}
                return("welcome back "+check[1]+" have a nice time.")
            else:
                return("incorrect password or username. please try again.")
        if perm.isowner(input) and check[0]=='groupset':
            if check[2] in ["admin","superadmin","owner"] and usercheck==check[1] and check[2] in ["admin","superadmin","owner"]:
                db_global.execute("delete from auth where user=(?)", (check[1],)).rowcount
                db_global.execute("insert or replace into auth(user, pass, groups) values (?,?,?)",(check[1], passcheck,check[2]))
                db_global.commit()
                del bot.auth[str(conn.name)][groupcheck][str(input.nick)]
                bot.auth[str(conn.name)][check[2]][str(input.nick)]={}
                return("done. group set to "+check[2])
            else:
                return("user not found or group not found.")
        if perm.isowner(input) and check[0]=='set' and usercheck==check[1] and check[2]:
            if usercheck==check[1]:
                db_global.execute("delete from auth where user=(?)", (check[1],)).rowcount
                db_global.execute("insert or replace into auth(user, pass, groups) values (?,?,?)",(check[1], hashlib.sha512(check[2]).hexdigest(),groupcheck))
                db_global.commit()
                return("done. reset password.")
            else:
                return("user not found.")
        if check[0]=='reset' and usercheck==check[1] and passcheck==hashlib.sha512(check[2]).hexdigest() and check[3]:
            db_global.execute("delete from auth where user=(?)", (check[1],)).rowcount
            db_global.execute("insert or replace into auth(user, pass, groups) values (?,?,?)",(check[1], hashlib.sha512(check[3]).hexdigest(),groupcheck))
            db_global.commit()
            return("done. reset you password.")
    else:
        return("error. try ,auth help")
        
        
# auth tracking has been moved here.
        
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
        if old in bot.auth[str(conn.name)][groupcheck]:
            bot.auth[str(conn.name)][groupcheck][str(new)]={}
            del bot.auth[str(conn.name)][groupcheck][str(old)]
            
def userquit(nick,conn,bot):
    for groupcheck in groupscheck:
        if nick in bot.auth[str(conn.name)][groupcheck]:
            del bot.auth[str(conn.name)][groupcheck][str(nick)]

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