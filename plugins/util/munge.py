# -*- coding: utf-8 -*-
from util import hook

character_replacements = {
    '1': 'ĺ',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    '0': 'Ö',
    'a': 'ä',
    'b': 'Б',
    'c': 'ċ',
    'd': 'đ',
    'e': 'ë',
    'f': 'ƒ',
    'g': 'ġ',
    'h': 'ħ',
    'i': 'í',
    'j': 'ĵ',
    'k': 'ķ',
    'l': 'ĺ',
    'm': 'ṁ',
    'n': 'ñ',
    'o': 'ö',
    'p': 'ρ',
    'q': 'ʠ',
    'r': 'ŗ',
    's': 'š',
    't': 'ţ',
    'u': 'ü',
    'v': 'v',
    'w': 'ω',
    'x': 'χ',
    'y': 'ÿ',
    'z': 'ź',
    'A': 'Å',
    'B': 'Β',
    'C': 'Ç',
    'D': 'Ď',
    'E': 'Ē',
    'F': 'Ḟ',
    'G': 'Ġ',
    'H': 'Ħ',
    'I': 'Í',
    'J': 'Ĵ',
    'K': 'Ķ',
    'L': 'Ĺ',
    'M': 'Μ',
    'N': 'Ν',
    'O': 'Ö',
    'P': 'Р',
    'Q': 'Ｑ',
    'R': 'Ŗ',
    'S': 'Š',
    'T': 'Ţ',
    'U': 'Ů',
    'V': 'Ṿ',
    'W': 'Ŵ',
    'X': 'Χ',
    'Y': 'Ỳ',
    'Z': 'Ż'}

def mungess(input):
    nickf = input
    reps = 0
    rep = ""
    for n in xrange(len(nickf)):
        rep = character_replacements.get(nickf[n])
        if rep:
            nickf = nickf[:n] + rep.decode('utf-8') + nickf[n + 1:]
            reps = reps + 1
            if reps == munge_count:
                break
    if input.nick:
        return nickf[0]+input.nick[1:]
    else:
        return nickf
    
def munge(munge_count, input, bot, reps, rep):
    nickf = input.nick
    reps = 0
    rep = ""
    for n in xrange(len(nickf)):
        rep = character_replacements.get(nickf[n])
        if rep:
            nickf = nickf[:n] + rep.decode('utf-8') + nickf[n + 1:]
            reps = reps + 1
            if reps == munge_count:
                break
    if input.nick:
        return nickf[0]+input.nick[1:]
    else:
        return nickf

def minp(munge_count, input, bot, reps, rep):
    nickf = input.inp
    reps = 0
    rep = ""
    for n in xrange(len(nickf)):
        rep = character_replacements.get(nickf[n])
        if rep:
            nickf = nickf[:n] + rep.decode('utf-8') + nickf[n + 1:]
            reps = reps + 1
            if reps == munge_count:
                break
    if input.nick:
        return nickf[0]+input.inp[1:]
    else:
        return nickf
    
def muninput(input, bot, inpset):
    munge_count = 0
    nickf = inpset
    reps = 0
    rep = ""
    for n in xrange(len(nickf)):
        rep = character_replacements.get(nickf[n])
        if rep:
            nickf = nickf[:n] + rep.decode('utf-8') + nickf[n + 1:]
            reps = reps + 1
            if reps == munge_count:
                break
    if input.nick:
        return nickf[0]+inpset[1:]
    else:
        return nickf