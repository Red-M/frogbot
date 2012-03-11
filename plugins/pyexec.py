import re

from util import hook, http
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
    return ret

def rexec(s, bot, input, db):
    try:
        exec(s)
    except:
        print s
        raise


@hook.command
def ply(inp, bot=None, input=None, nick=None, db=None, chan=None):
    "execute local python - only admins can use this"
    if not usertracking.query(db, bot.config, nick, chan, "ply") or not input.nick=="Red_M":
        return "nope.avi"
    try:
	
        _blah = dict(globals())
	_blah.update(input)
	_blah.update(locals())
        exec inp in _blah
        return _blah["_r"] if "_r" in _blah else None
    except:
        import traceback
        s = traceback.format_exc()
        sp = [x for x in s.split("\n") if x]
        if len(sp) > 2: sp = sp[-2:]
        for i in sp:
            input.notice(i)
