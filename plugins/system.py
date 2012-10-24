import os
import re
import time
import string
import platform
import subprocess
from util import hook, perm
from datetime import timedelta

def replace(text, wordDic):
    rc = re.compile('|'.join(map(re.escape, wordDic)))

    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)

def checkProc(checked_stats):
        status_file = open('/proc/self/status').read()
        line_pairs = re.findall(r'^(\w+):\s*(.*)\s*$', status_file, re.M)
        status = dict(line_pairs)
        checked_stats = checked_stats.split()
        stats = '\x02, '.join(key + ': \x02' + status[key] for key in checked_stats)#\x034,1
        input.say(stats)


@hook.command(autohelp=False)
def system(inp, input=None):
    ".system -- Retrieves information about the host system."
    if perm.isadmin(input):
        name = platform.node()
        os = platform.platform()
        python_version = platform.python_implementation() + ' ' + platform.python_version()
        arch = '-'.join(platform.architecture())
        cpu = platform.machine()
        input.say('Name: \x02%s\x02, Operating System: \x02%s\x02, Python Version: \x02%s\x02, Architecture: \x02%s\x02, CPU: \x02%s' % (name, os, python_version, arch, cpu))
        #input.say('Name: \x034,1\x02%s\x031,0\x02, Operating System: \x034,1\x02%s\x031,0\x02, Python Version: \x034,1\x02%s\x031,0\x02, Architecture: \x034,1\x02%s\x031,0\x02, CPU: \x034,1\x02%s' % (name, os, python_version, arch, cpu))
    else:
        input.say(input.nick+": Nope.avi")


@hook.command(autohelp=False)
def uptime(inp, bot=None):
    ".uptime -- Shows the bot's uptime."
    uptime_raw = round(time.time() - bot.start_time)
    uptime = timedelta(seconds=uptime_raw)
    return "Uptime: \x02%s\x02" % uptime #\x034,1

@hook.command(autohelp=False)
def pid(inp, input=None):
    ".pid -- Prints the bot's PID."
    input.say('PID: \x02%s' % os.getpid())
#    input.say('PID: \x034,1\x02%s\x034,1' % os.getpid())
