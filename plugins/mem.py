import os
import re

from util import hook
roundtonum=3

@hook.command(autohelp=False)
def vmem(inp, input=None):
    ",vmem -- returns bot's current memory usage -- linux/windows only"
    if os.name == "posix":
        # get process info
        status_file = open('/proc/self/status').read()
        s = dict(re.findall(r'^(\w+):\s*(.*)\s*$', status_file, re.M))
        # get the data we need and process it
        data = s['VmRSS'], s['VmSize'], s['VmPeak'], s['VmStk'], s['VmData']
        data = [float(i.replace(' kB', '')) for i in data]
        strings = []
        for i in data:
            if ((i/1024)<1):
                strings.append(str(int(i)) + ' kB')
            else:
                strings.append(str(round(i / 1024, roundtonum)) + ' MB')
        # prepare the output
        out = "Threads: \x02%s\x02, Real: \x02%s\x02, Alloc: \x02%s\x02, Peak " \
              "Alloc: \x02%s\x02, Stack: \x02%s\x02, Heap" \
              ": \x02%s\x02" % (s['Threads'], strings[0], strings[1], strings[2],
              strings[3], strings[4])
        # return output
        return out

    elif os.name == "nt":
        cmd = 'tasklist /FI "PID eq %s" /FO CSV /NH' % os.getpid()
        out = os.popen(cmd).read()
        memory = 0
        for amount in re.findall(r'([,0-9]+) K', out):
            memory += int(amount.replace(',', ''))
        memory = str(round(float(memory) / 1024, roundtonum))
        return "Memory Usage: \x02%s MB\x02" % memory

    else:
        return "Sorry, this command is not supported on your OS."
'''
    if os.name == 'posix':
        status_file = open("/proc/%d/status" % os.getpid()).read()
        s = dict(re.findall(r'^(\w+):\s*(.*)\s*$', status_file, re.M))
        line_pairs = re.findall(r"^(\w+):\s*(.*)\s*$", status_file, re.M)
        status = dict(line_pairs)
        keys = 'VmRSS VmSize VmLib VmData VmExe VmStk'.split()
        for key in keys:
            if (float(status[key].replace(" kB",""))/1024)>1:
                status[key]=str(float(status[key].replace(" kB",""))/1024)+" MB"
        input.say("Threads: \x02"+s['Threads']+"\x02, "+', '.join(key + ': ' + status[key]+"" for key in keys))
#        input.say(', '.join(key + ':\x034,2 ' + status[key]+"\x034,2" for key in keys))

    elif os.name == 'nt':
        cmd = "tasklist /FI \"PID eq %s\" /FO CSV /NH" % os.getpid()
        out = os.popen(cmd).read()

        total = 0
        for amount in re.findall(r'([,0-9]+) K', out):
            total += int(amount.replace(',', ''))

        input.say('memory usage: \x02'+str(float(total)/1024)+' MB')
#        input.say('memory usage: \x034,1\x02'+str(float(total)/1024)+' MB')
'''