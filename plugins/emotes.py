#written by 303

from util import hook
import re
import random
import usertracking

triggers = {}

def trigger(func):
    triggers[func.__doc__] = func
    return func

@trigger
def on_eat(match, input=None, **kw):
    r'eats\s+(?P<whom>\S+)'

    if match.group("whom").lower() == input.conn.nick.lower():
        reply = random.choice((
            "eats {0.nick}",
            "devours {0.nick} with gusto",
            "refuses to eat such filthy scum as {0.nick}",
            "tastes metallic",
        ))
        input.me(reply.format(input))

@trigger
def on_kick(match, input=None, bot=None, db=None, **kw):
    r'(?:kicks|hits)\s+(?P<whom>\S+)'

    if match.group("whom").lower() != input.conn.nick.lower():
        return

    if not usertracking.query(db, bot.config, input.nick, input.chan, "remotecontrol"):
        reply = random.choice((
            "{0.nick}: </3",
            "Ow :(",
            "I will remember this.",
            "What did I do? :<",
            "You will regret this.",
            "Ouch",
        ))
        input.say(reply.format(input))
        return

    input.say(random.choice((
        "Fine :<",
        "Bah",
        "If I must.",
        "Yes, master.",
    )))

    input.conn.send("PART %s :</3" % input.chan)

@trigger
def on_yawn(match, input=None, **kw):
    r'\byawns\b'
    reply = random.choice((
        "slaps {0.nick} - Wake up!",
        "hands {0.nick} a cup of coffee",
    ))
    input.me(reply.format(input))

@trigger
def on_slap(match, input=None, **kw):
    r'\bslaps\s+(?P<whom>\S+)'

    if match.group("whom").lower() != input.conn.nick.lower():
        return

    input.say("ow")

"""@hook.regex(r'(([^%/aeiou. ]+)[aeiuo][a-z]+) (you |)([^aeiou .]*([aeiuo][a-z]+))')
def do_thants(inp, input=None):
    input.say( "{0} {2}{3}... {1}{4}" .format( *inp.groups()))
"""

@hook.regex(r'\x01ACTION (.+)\x01')
@hook.command("trigger")
def do_trigger(inp, db=None, bot=None, input=None):
    match = inp.group(1)

    for pat, func in triggers.iteritems():
        m = re.search(pat, match)

        if m:
            func(m, input=input, db=db, bot=bot)
            return


