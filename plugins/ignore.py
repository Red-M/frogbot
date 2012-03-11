from util import hook
import botmodes


@hook.sieve
def ignore(bot, input, func, kind, args):
    channel = None
    if input.chan in input.conn.users.channels:
        channel = input.users.channels[input.chan]
    user = None
    if input.nick in input.conn.users.users:
        user = input.conn.users.users[input.nick]
    c = botmodes.Checker(bot, user, channel)
    db = bot.get_db_connection(input.conn)
    if c.check("neverquiet." + kind, db):
        return input
    if c.check("quiet." + kind, db):
        return
    return input