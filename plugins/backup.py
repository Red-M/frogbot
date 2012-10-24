# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook
import datetime
import ftplib
import time
from itertools import izip
from util import perm
import dircache
import thread
ftplock = thread.allocate_lock()

@hook.singlethread
@hook.command
def backup(inp, input=None, conn=None):
    ",backup -- makes the bot automatically back up it's data base every 3 hours into the location set in the configs. bot owner only."
    if perm.isowner(input):
        repnick=input.nick
        testss = True
        list = dircache.listdir(input.bot.persist_dir)
        while testss:
            if not ftplock.acquire(): raise Exception("Problem acquiring ftplock, probable thread crash. Abort.")
            try:
                testss = False
                filedir = ''
                ftp_pw = ''.join(input.conn.conf["ftp_pw"])
                if ftp_pw:
                    if ftp_pw in input.bot.config['censored_strings']:
                        input.bot.config['censored_strings'].remove(ftp_pw)
                x=-1
                list2=[]
                for file in list:
                    if str(file).endswith(".db"):
                        x=x+1
                        list2.append(str(file))
                ftp_host = ''.join(input.conn.conf["ftp_host"])
                ftp_user = ''.join(input.conn.conf["ftp_user"])
                ftp_port = input.conn.conf["ftp_port"]
                now = datetime.datetime.now()
                day = now.strftime("%Y%m%d_%H")
                ftp = ftplib.FTP()
                ftp.connect(ftp_host,ftp_port)
                ftp.login(ftp_user, ftp_pw)
                ftp.cwd(''.join(input.conn.conf["ftp_dir"]))
                print(ftp.dir())
                dirlists=str(ftp.dir())
                print(unicode(dirlists))
                if dirlists==None:
                    dirlists="nothing."
                if day in dirlists:
                    ftp.rmd(day)
                    ftp.mkd(day+"_2")
                if day not in dirlists:
                    ftp.mkd(day)
                ftp.cwd(day)
                for file in list2:
                    file_bu = open(str(input.bot.persist_dir)+"/"+str(file) ,'rb')
                    ftp.storbinary('STOR '+str(file).replace(".db","")+".."+ day +'..db' , file_bu)
                    file_bu.close()
                ftp.quit()
                input.bot.config['censored_strings'].append(ftp_pw)
                input.conn.send("PRIVMSG "+repnick+" done.")
                input.conn.send("PRIVMSG "+repnick+" :waiting for "+str(3)+" hours before backing up again!")
                time.sleep(2)
                time.sleep(3600*3)
                input.conn.send("PRIVMSG "+repnick+" :waiting done.")
                input.conn.send("PRIVMSG "+repnick+" :doing another backup.")
                testss = True 
            except:
                raise
            finally:
                ftplock.release()
    if not perm.isowner(input):
        input.conn.send("PRIVMSG "+input.nick+" Nope.avi")
        input.conn.send("PRIVMSG "+repnick+" :"+input.nick+" tried to use the auto backup command.")