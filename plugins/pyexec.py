import re

from util import hook, http, perm
import usertracking
import sys

import time

re_lineends = re.compile(r'[\r\n]*')

@hook.command
def python(inp, prefix="direct call", conn=None, nick=None):
    ".python <prog> -- executes python code <prog>"

#    if conn:
#        conn.send("PRIVMSG lahwran :%s pyexec: %s" % (prefix, inp))
    preres = http.get("http://eval.appspot.com/eval", statement=inp, nick=prefix)
    res = preres.splitlines()
    if len(res) > 0:
        res[0] = re_lineends.split(res[0])[0]
        if not res[0] == 'Traceback (most recent call last):':
            ret = res[0].decode('utf8', 'ignore')
        else:
            ret = res[-1].decode('utf8', 'ignore')
    else:
        ret = None
    if not ret: 
        return ("<reply>" if prefix == "direct call" else "") + "no return! try again, perhaps?"
    #print preres
    return ret

def rexec(s, bot, input, db):
    try:
        exec(s)
    except:
        print s
        raise
		
		
def runcode(code,glo):
	return eval(code,glo)


@hook.command
def ply(inp, bot=None, input=None, nick=None, db=None, chan=None):
	"execute local python - only admins can use this"
	if not perm.isadmin(input):
		return "Nope.avi"
	try:
		igncmds=["sys.stdout",'send("quit")',"send('quit')",'conn.connect()',"bot.conns[",'conf["ftp_pw"]','config["censored_strings"]','conf["server_password"]','conf["nickserv_password"]',"conf['ftp_pw']","config['censored_strings']","conf['server_password']","conf['nickserv_password']"]
		for data in igncmds:
			if str(data) in input.inp:
				return "Nope.avi"
		_blah = dict(globals())
		_blah.update(input)
		runcode(inp, _blah)
		if "_r" in _blah:
			out = _blah["_r"]
			igncmds=["sys.stdout",'send("quit")',"send('quit')",'conn.connect()',"bot.conns[",'conf["ftp_pw"]','config["censored_strings"]','conf["server_password"]','conf["nickserv_password"]',"conf['ftp_pw']","config['censored_strings']","conf['server_password']","conf['nickserv_password']"]
			for data in igncmds:
				if str(data) in input.inp:
					return "Nope.avi"
	except:
		import traceback
		s = traceback.format_exc()
		sp = [x for x in s.split("\n") if x]
		if len(sp) > 2: sp = sp[-2:]
		p=0
		for i in sp:
			p=p+1
			if p==1 and "^" in i:
				input.notice(i.replace(" ","_"))
			else:
				input.notice(i)
