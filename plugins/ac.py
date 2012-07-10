# plugin by Red_M on irc.esper.net or Red-M on github.
from util import hook, perm
import time
import dircache

@hook.command
def nasf(inp, bot=None, input=None):
	"checks to see if the bot cares about what you asked..."
	if perm.isadmin(input):
		return ("%s: Multiple cares found about %s" % (input.nick,
                                                            input.inp))
	else:
		return ("%s: Not a single care was found about%s" % (input.nick,
                                                                input.inp))