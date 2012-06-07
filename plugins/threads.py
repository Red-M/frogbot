#plugin made by Red-M on github or Red_M on esper.net
#this plugin makes sure that the bot stays connected to each IRC server or just the one.
from util import hook
import thread, time

threadss_userlock = thread.allocate_lock()

@hook.singlethread
@hook.event('004')
def thread_checks(inp, bot=None):
    if not threadss_userlock.acquire(): raise Exception("Problem acquiring thread_check_lock, probable thread crash. Abort.")
    try:
        while True:
            for xcon in bot.conns:
                bot.conns[xcon].send("PING :"+bot.conns[xcon].server)
            time.sleep(60)
    except:
        raise
    finally:
        threadss_userlock.release()
    