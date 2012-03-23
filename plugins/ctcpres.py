from util import hook


# CTCP responses
@hook.regex(r'^\x01VERSION\x01$')
def ctcpversion(inp, notice=None):
    notice('VERSION: Frogbot (custom build)/(dev build) -- https://github.com/Red-M/frogbot')


@hook.regex(r'^\x01PING\x01$')
def ctcpping(inp, notice=None):
    notice('\x01PING: PONG')


@hook.regex(r'^\x01TIME\x01$')
def ctcptime(inp, notice=None):
    notice('\x01TIME: GET A WATCH')


@hook.regex(r'^\x01FINGER\x01$')
def ctcpfinger(inp, notice=None):
    notice('\x01FINGER: WHERE ARE YOU PUTTING THAT')
