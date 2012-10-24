import re
import socket
import subprocess
import time

from util import hook, http, munge, perm
socket.setdefaulttimeout(10)  # global setting


def get_version():
    ret = 'Frogbot.'

    return ret


#autorejoin channels
#@hook.event('KICK')
#def rejoin(paraml, conn=None):
#    if paraml[1] == conn.nick:
#        if paraml[0].lower() in conn.channels:
#            conn.join(paraml[0])


#join channels when invited
@hook.event('INVITE')
def invite(paraml, conn=None, input=None, bot=None):
    repchan = input.conn.conf["reportchan"]
    nickf = munge.munge(0, input, bot, 0, "")
    if paraml[-1] == "#bottestspamchan":
        return "no."
    conn.join(paraml[-1])


@hook.event('004')
def onjoin(paraml, conn=None, bot=None, input=None):
    input.conn.send("NICK "+conn.conf["nick"])
    # identify to services
    nickserv_password = conn.conf.get('nickserv_password', '')
    nickserv_name = conn.conf.get('nickserv_name', 'nickserv')
    nickserv_command = conn.conf.get('nickserv_command', 'IDENTIFY %s')
    nickserv_command2 = conn.conf.get('nickserv_command', 'REGAIN %s %s')
    if nickserv_password:
        if nickserv_password in bot.config["censored_strings"]:
            for num in str(bot.config["censored_strings"].count(nickserv_password)):
                bot.config["censored_strings"].remove(nickserv_password)
        conn.msg(nickserv_name, "REGAIN "+conn.nick+" "+nickserv_password)
        conn.msg(nickserv_name, nickserv_command % nickserv_password)
        time.sleep(1)

    # set mode on self
    mode = conn.conf.get('mode')
    if mode:
        conn.cmd('MODE', [conn.nick, mode])

    # join channels
    for channel in conn.channels:
        conn.send('JOIN '+channel)
        time.sleep(.1)  # don't flood JOINs

    # set user-agent
    rev = get_version()


@hook.regex(r'^\x01VERSION\x01$')
def version(inp, notice=None):
    rev = get_version()
    
