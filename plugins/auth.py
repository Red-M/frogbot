# auth plugin written by Red-M on github or Red_M on esper.net
from util import hook, perm
import hashlib


@hook.command#(owneronly=True)
def auth(inp, input=None, db_auth=None, bot=None, conn=None):
    "auth with this bot. NOTE: no password is stored in plain text. all passwords are stored as a md5 hash. usage: ,auth login <username> <password>"
    db_auth.execute("create table if not exists auth(user, pass, groups)")
    db_auth.commit()
    check=input.inp.split(' ')
    #print(check)
    if len(check)==1 and check[0]=="help":
        out="To register with "+conn.nick+" please use ,auth <signup/reg> <username-you-want> <password-you-want>"
        out=out+". To login with "+conn.nick+" please use ,auth login <username-you-set> <password-you-set>"
        out=out+". If you forgot your password please contact "+conn.conf["owner"][0]+" about it."
        return(out)
    if len(check)==2 and check[0]=="logout":
        groupcheck=''.join(str(db_auth.execute("select groups from auth where user=(?)",(check[1],)).fetchone()[0]))
        if input.nick in bot.auth[str(conn.server)][groupcheck]:
            del bot.auth[str(conn.server)][groupcheck][str(input.nick)]
            return "Bye!"
    if len(check)>=3:
        cmdlist=["login",'groupset','set','reset']
        if check[0] in cmdlist:
            usercheck=''.join(str(db_auth.execute("select user from auth where user=(?)",(check[1],)).fetchone()[0]))
            passcheck=''.join(str(db_auth.execute("select pass from auth where user=(?)",(check[1],)).fetchone()[0]))
            groupcheck=''.join(str(db_auth.execute("select groups from auth where user=(?)",(check[1],)).fetchone()[0]))
        #print(usercheck+"\n"+passcheck+'\n'+groupcheck)
        if check[0]=='reg' or check[0]=='signup':
            usercheck=''.join(str(db_auth.execute("select user from auth where user=(?)",(check[1],)).fetchone()))
            passcheck=''.join(str(db_auth.execute("select pass from auth where user=(?)",(check[1],)).fetchone()))
            groupcheck=''.join(str(db_auth.execute("select groups from auth where user=(?)",(check[1],)).fetchone()))
            check[2]=hashlib.md5(check[2]).hexdigest()
            if check[1]==str(usercheck):
                return("you are already registered on this bot or choose another name.")
            else:
                db_auth.execute("insert into auth(user, pass, groups) values (?,?,?)",(check[1], check[2],"none"))
                db_auth.commit()
                perm.repamsg(input,input.nick+" is registering with me.")
                return("done. please login by using ,auth login "+check[1]+" <password-here>.")
        if check[0]=="login":
            print(input.nick+" is trying to auth as "+check[1])
            hashcheck=hashlib.md5(check[2]).hexdigest()
            if usercheck==check[1] and passcheck==hashcheck:
                print(groupcheck)#if groupcheck==None
                bot.auth[str(conn.server)][groupcheck][str(input.nick)]={}
                return("welcome back "+check[1]+" have a nice time.")
            else:
                return("incorrect password or username. please try again.")
        if perm.isowner(input) and check[0]=='groupset':
            if check[2] in ["admin","superadmin","owner"] and usercheck==check[1] and check[2] in ["admin","superadmin","owner"]:
                db_auth.execute("delete from auth where user=(?)", (check[1],)).rowcount
                db_auth.execute("insert or replace into auth(user, pass, groups) values (?,?,?)",(check[1], passcheck,check[2]))
                db_auth.commit()
                del bot.auth[str(conn.server)][groupcheck][str(input.nick)]
                bot.auth[str(conn.server)][check[2]][str(input.nick)]={}
                return("done. group set to "+check[2])
            else:
                return("user not found or group not found.")
        if perm.isowner(input) and check[0]=='set' and usercheck==check[1] and check[2]:
            if usercheck==check[1]:
                db_auth.execute("delete from auth where user=(?)", (check[1],)).rowcount
                db_auth.execute("insert or replace into auth(user, pass, groups) values (?,?,?)",(check[1], hashlib.md5(check[2]).hexdigest(),groupcheck))
                db_auth.commit()
                return("done. reset password.")
            else:
                return("user not found.")
        if check[0]=='reset' and usercheck==check[1] and passcheck==hashlib.md5(check[2]).hexdigest() and check[3]:
            db_auth.execute("delete from auth where user=(?)", (check[1],)).rowcount
            db_auth.execute("insert or replace into auth(user, pass, groups) values (?,?,?)",(check[1], hashlib.md5(check[3]).hexdigest(),groupcheck))
            db_auth.commit()
            return("done. reset you password.")
    else:
        return("error. try ,auth help")