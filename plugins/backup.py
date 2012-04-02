# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook
import datetime
import ftplib
import time
from itertools import izip
from util import perm

@hook.command
def up(inp, input=None):
	"Nothing to see here. Move along."
	if perm.isowner(input):
		repnick=input.nick
		testss = True
		while testss:
			testss = False
			filedir = '/shares/mc/bot'
			bu = './persist/frog.db'
			ftp_host = 'redmun.dyndns.org'
			ftp_user = 'admin'
			ftp_pw = 'danb17'
			ftp_port = 25563
			now = datetime.datetime.now()
			day = now.strftime("%Y%m%d_%H")
			ftp = ftplib.FTP()
			ftp.connect(ftp_host,ftp_port)
			ftp.login("admin", "danb17")
			ftp.cwd("./mc/bot")
			file_bu = open(bu ,'rb')
			ftp.storbinary('STOR backup'+ day +'.db' , file_bu)
			file_bu.close()
			ftp.quit()
			input.conn.send("PRIVMSG Red_M done.")
			input.conn.send("PRIVMSG Red_M :waiting for "+str(3)+" hours before backing up again!")
			time.sleep(2)
			time.sleep(3600*3)
			input.conn.send("PRIVMSG Red_M :waiting done.")
			input.conn.send("PRIVMSG Red_M :doing another backup.")
			testss = True 
	if not perm.isowner(input):
		input.conn.send("PRIVMSG "+input.nick+" Nope.avi")
        input.conn.send("PRIVMSG Red_M :"+input.nick+" tried to use the auto backup command.")