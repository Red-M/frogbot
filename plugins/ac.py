# plugin by Red_M
from util import hook
import os
import datetime
import tarfile
import smtplib
import ftplib
import time
import re
from itertools import izip

repnick = "Red_M"#bot owner nick here

@hook.command
def adm(inp, bot=None, input=None):
	outos=str(bot.config["admins"])
	outos=outos.replace("u'","")
	outos=outos.replace("'","")
	outos=outos.replace("[","")
	outos=outos.replace("]","")
	input.conn.send("PRIVMSG "+ input.chan +" :The Admins of this bot are: "+outos)


@hook.command
def chan(inp, input=None, db=None, bot=None, users=None):
        outrs=str(users.channels.keys())
        outrs=outrs.replace("u'","")
        outrs=outrs.replace("'","")
        outrs=outrs.replace("[","")
        outrs=outrs.replace("]","")
        input.conn.send("PRIVMSG "+ input.chan +" :I am in these channels: "+outrs)
       

@hook.command
def gtfo(inp, input=None):
       if input.nick in input.bot.config["admins"]:
               input.conn.send("PART "+input.chan)
       else:
               input.conn.send("PRIVMSG "+input.nick+" :You cannot do this.")



@hook.command
def nasf(inp, input=None):
	"checks to see if a single fuck was given."
	if input.nick in input.bot.config["admins"]:
		input.conn.send("PRIVMSG " + input.chan + " :" + input.nick + " numerous fucks found.")
        else:
            if input.nick not in input.bot.config["admins"]:
                input.conn.send("PRIVMSG " + input.chan + " :" + input.nick + " error: not a single fuck was found.")
        

@hook.command
def kl(inp, say=None, nick=None, input=None):
    "kills me."
    if not input.nick==repnick:
        input.notice("Only bot admins can use this command!")
    elif input.nick==repnick:
        input.conn.send('QUIT :Kill switch activated by Red_M.')
        time.sleep(3)
        os.abort()

@hook.command
def rl(inp, say=None, input=None):
    "restarts me."
    if input.nick not in input.bot.config["admins"]:
         input.notice("Only bot admins can use this command!")
    elif input.nick in input.bot.config["admins"]:
       input.conn.send('QUIT :Restart switch activated by '+input.nick+'.')
       os.system("screen python2.6 ./bot.py")
       time.sleep(3)
       os.abort()

@hook.command
def ac(inp, input=None):
    "asks crow something."
    if not inp == "":
        input.conn.send("PRIVMSG crow :?" + inp + " > " + input.nick)
    if not input.nick==repnick:
        input.conn.send("PRIVMSG "+repnick+" :"+input.nick+" has asked crow ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.") 

@hook.command
def aw(inp, input=None):
    "asks wololo something."
    if not inp == "":
        input.conn.send("PRIVMSG wololo :?" + inp + " > " + input.nick)
    if not input.nick==repnick:
        input.conn.send("PRIVMSG "+repnick+" :"+input.nick+" has asked wololo ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.") 

@hook.command
def ab(inp, input=None):
    ".ab <botnick> <factoid> -- asks <botnick> <factoid>."
    if not inp == "":
        botn = inp.split(" ")
        botn = botn[0]
        input.conn.send("PRIVMSG "+botn+" :?" + inp + " > " + input.nick)  
    if not input.nick==repnick:     
        input.conn.send("PRIVMSG "+repnick+" :"+input.nick+" has asked "+botn+" ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.")   
			
					
@hook.command
def up(inp, input=None):
	if input.nick==repnick:
		testss = True
		while testss:            
			print "1"
			testss = False
			print "2"
			filedir = './dir to backup to' # directory to backup to on the ftp
			bu = './persist/'+input.bot.config["connections"]["local irc"]["nick"]+'.db' # only change this if you know what this is.
			ftp_host = 'host name' #ftp hostname or url
			ftp_user = 'username' #ftp username
			ftp_pw = 'password' #ftp pass
			ftp_port = 25563 # port of the ftp
			now = datetime.datetime.now()
			day = now.strftime("%Y%m%d_%H")
			ftp = ftplib.FTP()
			ftp.connect(ftp_host,ftp_port)
			ftp.login(ftp_user, ftp_pw)
			ftp.cwd(filedir)
			file_bu = open(bu ,'rb')
			ftp.storbinary('STOR backup'+ day +'.db' , file_bu)
			file_bu.close()
			ftp.quit()
			input.conn.send("PRIVMSG "+repnick+" done.")
			input.conn.send("PRIVMSG "+repnick+" :waiting for "+str(3)+" hours before backing up again!")
			time.sleep(2)
			print "3"
			time.sleep(3600*3)
			input.conn.send("PRIVMSG "+repnick+" :waiting done.")
			input.conn.send("PRIVMSG "+repnick+" :doing another backup.")
			print "4"
			testss = True 
	if not input.nick==repnick:
		input.conn.send("PRIVMSG "+input.nick+" Nope.avi")
        input.conn.send("PRIVMSG "+repnick+" :"+input.nick+" tried to use the auto backup command.")