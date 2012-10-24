#written by 303 edits by Red_M on espernet or Red-M on github

from util import hook, perm
import re
import time
import random
import usertracking

triggers = {}

def trigger(func):
    triggers[func.__doc__] = func
    return func

@trigger
def on_eat(match, input=None, **kw):
    r'^eats\s+(?P<whom>\S+)'

    if match.group("whom").lower() == input.conn.nick.lower().replace(".",""):
        reply = random.choice((
            "eats {0.nick}",
            "devours {0.nick} with gusto",
            "refuses to eat such filthy scum as {0.nick}",
            "tastes metallic",
        ))
        input.me(reply.format(input))
        
@trigger
def on_pet(match, input=None, **kw):
    r'pets\s+(?P<whom>\S+)'

    if match.group("whom").lower() == input.conn.nick.lower():
        reply = random.choice((
            "purrs like a kitten.",
            "curls up.",
            "meow.",
            "*as Gir* HI FLOOR! make me a sammich.",
        ))
        if reply=="curls up.":
            input.me(reply.format(input))
            time.sleep(1.5)
            input.me("FLUFFS")
        else:
            input.me(reply.format(input))

@trigger
def on_kick(match, input=None, bot=None, db=None, **kw):
    r'(?:kicks|hits)\s+(?P<whom>\S+)'

    if match.group("whom").lower() != input.conn.nick.lower():
        return

    if not perm.isadmin(input):
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
        "*as Gir* Im sorry master...",
        "*as Gir* HI FLOOR! make me a sammich.",
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
    r'\bbeats\s+(?P<whom>\S+)'

    if match.group("whom").lower() != input.conn.nick.lower():
        return
    if not perm.isadmin(input):
        reply = random.choice((
            "{0.nick}: </3",
           "Ow :(",
           "I will remember this.",
           "What did I do? :<",
          "Why? Why, {0.nick}?",
           "Ouch",
        ))
        input.say(reply.format(input))
        return
    input.say(random.choice((
        "Fine :<",
        "meow...",
        "Yes all mighty lord.",
        "Yes, master.",
        "*as Gir* Im sorry master...",
        "*as Gir* HI FLOOR! make me a sammich.",
    )))
    return

@trigger
def on_slap(match, input=None, **kw):
    r'\bslaps\s+(?P<whom>\S+)'

    if match.group("whom").lower() != input.conn.nick.lower():
        return
    if not perm.isadmin(input):
        reply = random.choice((
           "slaps {0.nick}",
           "slaps {0.nick} bitch please.",
           "What did I do? :<",
           "Why? Why, {0.nick}?",
           "throws {0.nick} into the sun.",
        ))
        input.say(reply.format(input))
        return
    input.say(random.choice((
        "Fine :<",
        "meow...",
        "Yes all mighty lord.",
        "Yes, master.",
        "*as Gir* Im sorry master...",
        "*as Gir* HI FLOOR! make me a sammich.",
    )))
    return

"""@hook.regex(r'(([^%/aeiou. ]+)[aeiuo][a-z]+) (you |)([^aeiou .]*([aeiuo][a-z]+))')
def do_thants(inp, input=None):
    input.say( "{0} {2}{3}... {1}{4}" .format( *inp.groups()))
"""

@hook.regex(r'\x01ACTION (.+)\x01')
#@hook.command("trigger")
def do_trigger(inp, db=None, bot=None, input=None):
    match = inp.group(1)

    for pat, func in triggers.iteritems():
        m = re.search(pat, match)

        if m:
            func(m, input=input, db=db, bot=bot)
            return


