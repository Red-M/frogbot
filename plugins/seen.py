" seen.py: written by sklnd in about two beers July 2009"
# edited by Red-M on github or Red_M on irc.esper.net 2012
import time
from util import hook, timesince

def db_init(db):
    db.execute("create table if not exists seen(name, said, time, chan)")
    db.commit()

@hook.command
def seen(inp, nick='', chan='', db_seen=None, input=None):
    ",seen <nick> -- Tell when a nickname was last in active in irc"
    if input.conn.nick.lower() == inp.lower():
        return("I'm right here, need something?")
    if inp.lower() == nick.lower():
        return("Yes, that's your nick ...")
    db_init(db_seen)
    last_seen = db_seen.execute("select name, said, time, chan from seen where name=lower(?)", (inp,)).fetchone()
    if last_seen:
        reltime = timesince.timesince(last_seen[2])
        if last_seen[0] != inp.lower():  # for glob matching
            inp = last_seen[0]
        return('%s was last seen %s ago in %s saying: %s' % (inp, reltime, last_seen[3], last_seen[1].replace("\x01ACTION",'"'+inp+': ').replace("\x01",'"')))
    else:
        return("User not in database")