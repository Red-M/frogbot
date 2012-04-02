import os
import re
import time
import string
import platform
import subprocess
from util import hook

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
        stats = '\x02, '.join(key + ': \x034,1 ' + status[key] for key in checked_stats)
        input.say(stats)


@hook.command(autohelp=False)
def system(inp, input=None):
    ".system -- Retrieves information about the host system."
    name = platform.node()
    os = platform.platform()
    python_version = platform.python_implementation() + ' ' + platform.python_version()
    arch = '-'.join(platform.architecture())
    cpu = platform.machine()
    input.say('Name: \x034,1 %s\x031,0, Operating System: \x034,1 %s\x031,0, Python Version: \x034,1 %s\x031,0, Architecture: \x034,1 %s\x031,0, CPU: \x034,1 %s' % (name, os, python_version, arch, cpu))


@hook.command(autohelp=False)
def memory(inp, input=None):
    ".memory -- Displays the bot's current memory usage."
    if os.name == 'posix':
        checked_stats = 'VmRSS VmSize VmPeak VmStk VmData'
        memory = checkProc(checked_stats)
        pretty_names = {'VmRSS': 'Real Memory', 'VmSize': 'Allocated Memory', 'VmPeak': 'Peak Allocated Memory', 'VmStk': 'Stack Size', 'VmData': 'Heap Size'}
        memory = replace(memory, pretty_names)
        memory = string.replace(memory, ' kB', '')
        memory = memory.split('\x034,1 ')
        numbers = [memory[i] for i in range(len(memory)) if i % 2 == 1]
        memory = [i for i in memory if i not in numbers]
        numbers = [str(round(float(i) / 1024, 2)) + ' MB' for i in numbers]
        memory = [list(i) for i in zip(memory, numbers)]
        memory = sum(memory, [])
        memory = '\x034,1 '.join(memory)

    elif os.name == 'nt':
        cmd = 'tasklist /FI \"PID eq %s\" /FO CSV /NH' % os.getpid()
        out = os.popen(cmd).read()
        memory = 0
        for amount in re.findall(r'([,0-9]+) K', out):
            memory += int(amount.replace(',', ''))
        memory = str(round(float(memory) / 1024, 2))
        memory = 'Memory Usage: \x034,1 %s MB\x034,1' % memory
    else:
        memory = 'error: operating system not currently supported'
    input.say(memory)


@hook.command(autohelp=False)
def uptime(inp, bot=None):
    ".uptime -- Shows the bot's uptime."
    uptime_raw = time.time() - bot.start_time
    uptime = time.strftime('%H:%M:%S', time.gmtime(uptime_raw))
    return "Uptime:\x034,1 %s" % uptime

@hook.command(autohelp=False)
def pid(inp, input=None):
    ".pid -- Prints the bot's PID."
    input.say('PID: \x034,1 %s\x034,1' % os.getpid())
