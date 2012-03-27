import os
import re

from util import hook


@hook.command(autohelp=False)
def umem(inp):
    ".mem -- returns bot's current memory usage -- linux/windows only"

    if os.name == 'posix':
        status_file = open("/proc/%d/status" % os.getpid()).read()
        line_pairs = re.findall(r"^(\w+):\s*(.*)\s*$", status_file, re.M)
        status = dict(line_pairs)
        keys = 'VmSize VmLib VmData VmExe VmRSS VmStk'.split()
        for key in keys:
            if (float(status[key].replace(" kB",""))/1024)>1:
                status[key]=str(float(status[key].replace(" kB",""))/1024)+" MB"
        return ', '.join(key + ':' + status[key] for key in keys)

    elif os.name == 'nt':
        cmd = "tasklist /FI \"PID eq %s\" /FO CSV /NH" % os.getpid()
        out = os.popen(cmd).read()

        total = 0
        for amount in re.findall(r'([,0-9]+) K', out):
            total += int(amount.replace(',', ''))

        return 'memory usage: %d MB' % total/1024

    return mem.__doc__
