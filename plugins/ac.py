# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook
import os
import datetime
import tarfile
import smtplib
import ftplib
import time
import re
from itertools import izip



@hook.command
def admins(inp, bot=None, input=None):
	outos=str(bot.config["admins"])
	outos=outos.replace("u'","")
	outos=outos.replace("'","")
	outos=outos.replace("[","")
	outos=outos.replace("]","")
	input.conn.send("PRIVMSG "+ input.chan +" :The Admins of this bot are: "+outos)

@hook.command
def users(inp, bot=None, input=None):
        outoss=(str(input.conn.users.users))
        outoss=outoss.replace("u'","")
        outoss=outoss.replace("'","")
        #comp = re.compile('^<User object at 0x1.*>$')
        #print str(comp) 
        outoss=outoss.replace("<User object at 0x1","")
        outoss=outoss.replace("{","")
        outoss=outoss.replace("}","")
        outoss=outoss.replace(": ","")

        input.say(str(outoss))


@hook.command
def chan(inp, input=None, db=None, bot=None, users=None):
        outrs=str(users.channels.keys())
        outrs=outrs.replace("u'","")
        outrs=outrs.replace("'","")
        outrs=outrs.replace("[","")
        outrs=outrs.replace("]","")
        input.conn.send("PRIVMSG "+ input.chan +" :I am in these channels: "+outrs)
     
@hook.command
def raw(inp, input=None):
       if (input.nick=="Red_M" and not len(inp)==0):
               input.conn.send(inp)
       else:
               input.conn.send("PRIVMSG "+input.nick+" :You cannot do this.")
  

@hook.command
def gtfo(inp, input=None):
       if input.nick in input.bot.config["admins"]:
               input.conn.send("PART "+input.chan)
       else:
               input.conn.send("PRIVMSG "+input.nick+" :You cannot do this.")


@hook.event("KICK")
def kickss(inp, input=None):
    if input.nick in input.bot.config['admins']:
        return"WHY! WHY! WHY HIM?!?!?!? OH GOD WHY!"
    else:
        return"oh god!"

#@hook.event("NICK")
def nickss(inp, input=None):
    outrs=str(input.conn.channels)
    outrs=outrs.replace("u'","")
    outrs=outrs.replace("'","")
    outrs=outrs.replace("[","")
    outrs=outrs.replace("]","")
    if input.nick in input.bot.config['admins'] and not input.nick=="Red_M":
        input.conn.send("PRIVMSG "+outrs+" :"+input.nick+" has decide to change their nick to "+input.chan+".")
    if input.nick=="Red_M":
        input.conn.send("PRIVMSG "+outrs+" :Master where did you go?")
    else:
        input.conn.send("PRIVMSG "+outrs+" :"+input.nick+" has decide to change their nick to "+input.chan+".")


@hook.command
def ac(inp, input=None):
    "asks crow something."
    if not inp == "":
        input.conn.send("PRIVMSG crow :?" + inp + " > " + input.nick)
    if not input.nick=="Red_M":
        input.conn.send("PRIVMSG Red_M :"+input.nick+" has asked crow ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.") 

@hook.command
def aw(inp, input=None):
    "asks wololo something."
    if not inp == "":
        input.conn.send("PRIVMSG wololo :?" + inp + " > " + input.nick)
    if not input.nick=="Red_M":
        input.conn.send("PRIVMSG Red_M :"+input.nick+" has asked wololo ?" + inp + " > " + input.nick)
    if inp == "":
        input.say("nothing has been asked. not sending.") 

@hook.command
def ab(inp, input=None):
    ".ab <botnick> <factoid> -- asks <botnick> <factoid>."
    if not inp == "":
        botn = inp.split(" ")
        botn = botn[0]
        input.conn.send("PRIVMSG "+botn+" :?" + inp + " > " + input.nick)  
    if not input.nick=="Red_M":     
        input.conn.send("PRIVMSG Red_M :"+input.nick+" has asked "+botn+" ?" + inp + " > " + input.nick)
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