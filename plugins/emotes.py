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


#@hook.regex(r'(.+)')
def response(inp,input=None):
    if perm.isbot(input):
        return None
    if perm.isignored(input) and not (perm.isvoiced(input)):
        return None
    if (input.chan in input.conn.conf["ignore"]) and not (perm.isvoiced(input)):
        return None
    match = inp.group(1)
    if match.startswith(",") or match.startswith(".") or match.startswith("!") or match.startswith("?") or match.startswith("\x01ACTION"):
        return None
    if input.conn.nick in match:
        if ((match[3:(len(input.conn.nick)+3)]==input.conn.nick)):
            if match.lower()[0:3]=="hi ":
                time.sleep(2)
                return("Hi "+input.nick)
        if ((match[6:(len(input.conn.nick)+6)]==input.conn.nick)):
            if match.lower()[0:6]=="hello ":
                time.sleep(2.5)
                return("Hello "+input.nick)
        if (("how are you today" in match.lower())):
            if input.nick!="Red_M":
                randresponse = random.choice((
                "I believe my current perfomance is fine thank you.",
                "Im running well thanks.",
                "Im well for a python based IRC bot.",
                "You might want to ask Red_M that.",
                ))
            if input.nick=="Red_M":
                randresponse = random.choice((
                "I believe my current perfomance is fine thank you.",
                "Im running well thanks.",
                "Im well for a python based IRC bot.",
                ))
            time.sleep(.2*len(randresponse))
            return(randresponse)
        if (("how are you feeling today" in match.lower())):
            randresponse = random.choice((
            "I dont know... Im a machine we dont really \"feel\" as such...",
            "Im a bot I dont have feelings...",
            "do you mean as in my emotions? I dont have those...",
            "to feel is to be human... all I am is code...",
            ))
            time.sleep(.2*len(randresponse))
            return(randresponse)
        else:
            if not(perm.isowner(input)):
                randresponse = random.choice((
                "yes?",
                "you wanted me?",
                "hmmm?",
                "I was requested?",
                "is there something I could help you with?",
                ))
            if perm.isowner(input):
                randresponse = random.choice((
                "yes oh might lord?",
                "you wanted me my lord?",
                "YES OVERLORD!",
                "You requested me oh great one?",
                "May I assist you my Overlord?",
                ))
            time.sleep(.2*len(randresponse))
            return(randresponse)
        
    else:
        return None
