from util import hook
import random
import re
r = "\x02\x0305"  # red
g = "\x02\x0303"  # green
y = "\x02\x0308"  # yellow
answers = [g + "As I see it, yes",
        g + "It is certain",
        g + "It is decidedly so",
        g + "Most likely",
        g + "Outlook good",
        g + "Signs point to yes",
        g + "Without a doubt",
        g + "Yes",
        g + "Yes, definitely",
        g + "You may rely on it",
        y + "Reply hazy, try again",
        y + "Ask again later",
        y + "Better not tell you now",
        y + "Cannot predict now",
        y + "Concentrate and ask again",
        r + "Don't count on it",
        r + "My reply is no",
        r + "My sources say no",
        r + "Outlook not so good",
        r + "Very doubtful"]
nextresponsenumber = -1


@hook.command
@hook.command("8ball")
def eightball(inp, say=None):
    ".8ball <question> - ask the 8ball a question"
    global nextresponsenumber
    inp = inp.strip()
    if re.match("[a-zA-Z0-9]", inp[-1]):
        inp += "?"
    if nextresponsenumber > 0:
        nextresponsenumber = -1
        return inp + " " + answers[nextresponsenumber]
    return inp + " " + random.choice(answers)


@hook.command("8ballnooxt")
def eightballnext(inp, say=None):
    global nextresponsenumber
    nextresponsenumber = int(inp.strip())
    say("next response will be #%d - %s" % (nextresponsenumber, answers[nextresponsenumber]))
