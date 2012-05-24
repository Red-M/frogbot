# -*- coding: utf-8 -*-


from util import hook, munge


@hook.command
def munge(inp, munge_count=0):
    nickf = munge.minp(munge_count, input, bot, 0, "")
    return nickf
