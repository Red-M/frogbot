# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook, perm

@hook.event("QUIT")
def quitss(inp, input=None, bot=None):
    on=0
    if on==1:
        if perm.isadmin(input):
            input.say("*as Gir* Master, where did you go? I can't see you!")
        else:
            input.say("Bye!")
		
@hook.event("PART")
def partss(inp, input=None, bot=None):
    on=0
    if on==1:
        if perm.isadmin(input):
            input.say("*as Gir* Master, where did you go? I can't see you!")
        else:
            input.say("Bye!")

@hook.event("JOIN")
def joinss(inp, input=None, bot=None):
    on=0
    if on==1:
        if perm.isadmin(input):
            input.say("*as Gir* ooh Hi Master!")
        else:
            if input.nick==input.conn.nick:
                input.say("")
            else:
                input.say("Hi there.")