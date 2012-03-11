from util import hook

import random
import string

import googlesearch

import time

lastcall = 0.0

@hook.command
def bored(inp):
    global lastcall
    curtime = time.time()
    if curtime < lastcall + 4.0:
        return #"called too recently! please wait %d seconds." % ((lastcall + 4.0) - curtime)
    lastcall = curtime

    searchfunc = random.choice([googlesearch.google, googlesearch.gis])

    pool = random.choice([string.lowercase, string.uppercase,
            string.hexdigits, string.letters + string.digits])

    length = random.randint(1,5)
    query = [random.choice(pool) for i in range(length)]
    query = "".join(query)
    query += " " + inp
    query = query.strip()

    return "Results for query '%s': %s" % (query, searchfunc(query))
