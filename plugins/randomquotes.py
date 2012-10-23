from util import hook, http, urlnorm
import re
import random

wordDic = {
'&#x27;': "'",
'&#x22;': '"',
'&#34;': '"',
'&#39;': '\'',
'&#38;': '&',
'&#60;': '<',
'&#62;': '>',
'&#171;': '«',
'&quot;': '"',
'&apos;': '\'',
'&amp;': '&',
'&lt;': '<',
'&gt;': '>',
'&laquo;': '«',
'&#33;': '!',
'&#036;': '$',
'  ': ' ',
"[<i>": "[",
"</i>]": "]"}

cave = r'>Cave Johnson</a></i>:(.+?)<br/>'
glados = r'>GLaDOS</a></i>:(.+?)<br/>'
wheatly = r'>Wheatley</a></i>:(.+?)<br/>'
gir = r'>Gir</a></i>:(.+?)<br/>'
zim = r'>Zim</a></i>:(.+?)<br/>'
yoda = r'>Yoda</a></i>:(.+?)<br/>'
sheldon = r'>Sheldon Cooper</a></i>:(.+?)<br/>'

def multiwordReplace(text, wordDic):
    rc = re.compile('|'.join(map(re.escape, wordDic)))
    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)

def regexmatch(text,regex):
    match = regex.match(text)
    if not match:
        return("")
    (matcho,) = match.groups()
    return(matcho)
    
def regexmatch2(text,regex):
    match = regex.findall(text)
    if not match:
        return("")
    matcho = match
    return(matcho)

@hook.command("rquote")
@hook.command
def randomquote(inp, input=None, bot=None):
    help = ",randomquote <person> -- gets random quotes. Currently allowed persons Cave Johnson, GLaDOS, Wheatley, Gir, Zim, Yoda, Sheldon Cooper"
    if inp=="":
        return(help)
    check = []
    check = inp.lower().split(" ")
    if check[0]=="cave":
        h = http.get('http://www.imdb.com/character/ch0242805/quotes').replace("\n","").replace("   ","").replace("  ","").replace("	","")
        return("Cave Johnson: "+multiwordReplace(random.choice(regexmatch2(h,re.compile(cave))),wordDic))
    if check[0]=="glados":
        h = http.get('http://www.imdb.com/character/ch0069595/quotes').replace("\n","").replace("   ","").replace("  ","").replace("	","")
        return("GLaDOS: "+multiwordReplace(random.choice(regexmatch2(h,re.compile(glados))),wordDic))
    if check[0]=="wheatley":
        h = http.get('http://www.imdb.com/character/ch0242806/quotes').replace("\n","").replace("   ","").replace("  ","").replace("	","")
        return("Wheatley: "+multiwordReplace(random.choice(regexmatch2(h,re.compile(wheatly))),wordDic))
    if check[0]=="gir":
        h = http.get('http://www.imdb.com/character/ch0131917/quotes').replace("\n","").replace("   ","").replace("  ","").replace("	","")
        return("Gir: "+multiwordReplace(random.choice(regexmatch2(h,re.compile(gir))).encode("utf8"),wordDic))
    if check[0]=="zim":
        h = http.get('http://www.imdb.com/character/ch0088128/quotes').replace("\n","").replace("   ","").replace("  ","").replace("	","")
        return("Zim: "+multiwordReplace(random.choice(regexmatch2(h,re.compile(zim))).encode("utf8"),wordDic))
    if check[0]=="yoda":
        h = http.get('http://www.imdb.com/character/ch0000015/quotes').replace("\n","").replace("   ","").replace("  ","").replace("	","")
        return("Yoda: "+multiwordReplace(random.choice(regexmatch2(h,re.compile(yoda))).encode("utf8"),wordDic))
    if check[0]=="sheldon":
        h = http.get('http://www.imdb.com/character/ch0064640/quotes').replace("\n","").replace("   ","").replace("  ","").replace("	","")
        return("Sheldon Cooper: "+multiwordReplace(random.choice(regexmatch2(h,re.compile(sheldon))).encode("utf8"),wordDic))
