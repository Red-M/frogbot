from util import hook, perm
import pyexec
import usertracking
import re
import time

redirect_re = re.compile(r'([|>])\s*(\S*)\s*$|([<])(.*)')
word_re = re.compile(r'^([+~-]?)(\S+)')
filter_re = re.compile(r'^\s*[<]([^>]*)[>]\s*(.*)\s*$')
cmdfilter_re = re.compile(r'^cmd:(.+)$')
forgotten_re = re.compile(r'^([<]locked[^>]*[>])?[<]forgotten[>].*')
maxdepth = 4

def db_init(db):
    db.execute("create table if not exists memory(chan, word, data, nick)")
    db.commit()

#@hook.regex(r'^[?!](.+)')  # groups: (mode,word,args,redirectmode,redirectto)
def question(inp, db=None, input=None,args=None):
    check = input.lastparam.split(' ')
    word = check[0].replace("?","")
    wordtype = ""
    dbdata = db.execute("select data from memory where chan=? and word=lower(?)",(input.chan, word)).fetchone()
    if not dbdata:
        dbdata = db.execute("select data from memory where word=lower(?)",(word,)).fetchone()
    if word.startswith("."):
        wordtype = "local"
    dbdata = ''.join(dbdata)
    variables = {"chan": input.chan or "","user": input.user or "","nick": input.conn.nick or "","inp": args or "","ioru": args or input.nick,"word": word or ""}
    
    print check
    for i in variables.keys():
        dbdata = dbdata.replace("$" + i, variables[i])
    preargs = ""
    for i in variables.keys():
        preargs += i + "=" + repr(unicode(variables[i]).encode('utf8')) + ";"
    print pyexec.python(preargs)
    print dbdata
