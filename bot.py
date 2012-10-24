#!/usr/bin/env python

a = 34123

__creator__ = "Red_M"
__credits__ = ["neersighted","Luke","Lahwran"]
__email__ = "pooatyou.com@gmail.com"
__web__ = "http://red-m.x10.mx"
__repo__ = "https://github.com/Red-M/frogbot"

import os
import Queue
import sys
import time

sys.path += ['plugins']  # so 'import hook' works without duplication
sys.path += ['core']  # so 'import IRC' works without duplication
sys.path += ['lib']
os.chdir(sys.path[0] or '.')  # do stuff relative to the install directory


class Bot(object):
    pass

print "Frogbot made by "+__creator__+" (email:"+__email__+")\nwebsite:"+__web__+" repo:"+__repo__
print "Frogbot had assitance from "+', '.join(__credits__)

bot = Bot()
bot.start_time = time.time()

print 'Loading plugins'

# bootstrap the reloader
eval(compile(open(os.path.join('core', 'reload.py'), 'U').read(),
    os.path.join('core', 'reload.py'), 'exec'))
reload(init=True)

config()
if not hasattr(bot, 'config'):
    exit()

print 'Connecting to IRC'

bot.conns = {}
bot.cooldown = {}
bot.auth = {}
bot.seen = {}
bot.chanseen = {}
bot.twitterlist = {}
bot.twitterlists = {}
bot.connected={}
bot.path=__file__

try:
    for name, conf in bot.config['connections'].iteritems():
        if conf.get('ssl'):
            bot.conns[name] = SSLIRC(conf['server'], conf['nick'], conf=conf,
                    port=conf.get('port', 6667), channels=conf['channels'],
                    ignore_certificate_errors=conf.get('ignore_cert', True),name=name)
        else:
            bot.conns[name] = IRC(conf['server'], conf['nick'], conf=conf,
                    port=conf.get('port', 6667), channels=conf['channels'],name=name)
except Exception, e:
    print 'ERROR: malformed config file', e
    sys.exit()

bot.term=False
for xcon in bot.conns:
    bot.cooldown[str(bot.conns[xcon].name)]={}
    bot.auth[str(bot.conns[xcon].name)]={}
    bot.auth[str(bot.conns[xcon].name)]["owner"]={}
    bot.auth[str(bot.conns[xcon].name)]["superadmin"]={}
    bot.auth[str(bot.conns[xcon].name)]["admin"]={}
    bot.auth[str(bot.conns[xcon].name)]["none"]={}
    bot.seen[str(bot.conns[xcon].name)]={}
    bot.connected[str(bot.conns[xcon].name)]=0
    bot.chanseen[str(bot.conns[xcon].name)]={}
    for channels in bot.conns[xcon].conf["channels"]:
        bot.chanseen[str(bot.conns[xcon].name)][channels]=["start-up"]
        
bot.persist_dir = os.path.abspath('persist')
bot.logs_dir = os.path.abspath('logs')
if not os.path.exists(bot.logs_dir):
    os.mkdir(bot.logs_dir)
if not os.path.exists(bot.persist_dir):
    os.mkdir(bot.persist_dir)

print 'Running main loop'

while True:
    if bot.term==True:
        sys.exit(0)
    reload()  # these functions only do things
    config()  # if changes have occured

    for conn in bot.conns.itervalues():
        try:
            out = conn.out.get_nowait()
            main(conn, out)
        except Queue.Empty:
            pass
    while all(conn.out.empty() for conn in bot.conns.itervalues()):
        time.sleep(.15)

