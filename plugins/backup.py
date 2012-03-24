# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook
import datetime
import ftplib
import time
from itertools import izip

@hook.command
def up(inp, input=None):
	if input.nick in input.bot.config["owner"]:
        repnick=input.nick
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