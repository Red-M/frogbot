# -*- coding: utf-8 -*-
# minecraft wiki scrapper made by Red_M on esper.net or Red-M on GitHub.com
# used parts of the SCP wiki scrapper to build this one...
from util import hook, http, urlnorm, perm
import re
import time

wordDic = {
str('{{Cleanup}}'): '',
str('{{cleanup}}'): '',
str('{{Snapshot}}'): '',
str('<onlyinclude>'): '',
str('{{stub}}'): '',
str('|'): ',',
str('<br>'): ',',
str('firstver='): 'First Version=',
str('data='): 'item id=',
str("'''"): '"',
str("ItemLink,"): '',
str("\nAn"): '',
str("\'\'"): '"'

}
wordDic2 = {
str('[['): '',
str(']]'): '',
str('{'): '',
str('{{'): '',
str('}'): '',
str('}}'): ''
}
        
def regexmatch2(text,regex):
    match = regex.match(text)
    if not match:
        return("")
    (matcho,) = match.groups()
    return matcho
    
def dbresponse(query,url,db_global):
    (desc, url, timemon, query) = db_global.execute("select desc, url, time, query from mcwiki where query=(?)",(query.lower(),)).fetchone()
    return("(Cached) "+desc)
    
def dataget(url):
    pageid = url['pages'].keys()[0]
    url = url['pages'][pageid][u'revisions'][0]['*']#.replace("\n","")
    if url.startswith("#REDIRECT "):
        return url
    textb = {}
    textb[regexmatch2(url,re.compile(r'.+?(\|sounds=.+?\}\}'+'\n\n'+')',re.DOTALL))] = ""
    for data in textb:
        url = url.replace(data,textb[data])
    url = url.replace("\n","")
    for dart in wordDic:
        url = url.replace(dart,wordDic[dart])
    for dart in wordDic2:
        url = url.replace(dart,wordDic2[dart])
    texta = {}
    if "health=hp," in url:
        texta[regexmatch2(url,re.compile(r'.+?\,(health=hp,)'))] = "health:"
    if "image=" in url:
        texta[regexmatch2(url,re.compile(r'.+?\,(image=.+?,)'))] = ""
    if "image2=" in url:
        texta[regexmatch2(url,re.compile(r'.+?\,(image2=.+?,)'))] = ""
    if "imagesize=" in url:
        texta[regexmatch2(url,re.compile(r'.+?\,(imagesize=.+?,)'))] = ""
    if "image2size=" in url:
        texta[regexmatch2(url,re.compile(r'.+?\,(image2size=.+?,)'))] = ""
    if "caption=" in url:
        texta[regexmatch2(url,re.compile(r'.+?\,(caption=.+?,)'))] = ""
    if "drops=" in url:
        texta[regexmatch2(url,re.compile(r'.+?\,(drops=.+?,)'))] = "Drops: "
    for data in texta:
        url = url.replace(data,texta[data])
    return url.replace(", ",",").replace(",",", ").replace("caption=,","")
    
def apiget(inp,url,requesturl,timemon,db_global):
    pageid = url['pages'].keys()[0]
    if not pageid=="-1":
        url = dataget(url)
        for dart in wordDic2:
            url = url.replace(dart,wordDic2[dart])
        while url.startswith("#REDIRECT "):
            url2 = http.get_json("http://www.minecraftwiki.net/api.php?format=json&action=query&titles="+url.replace("#REDIRECT ","").replace(" ","%20")+"&prop=revisions&rvprop=content")["query"]
            url = dataget(url2)
        db_global.execute("insert or replace into mcwiki(desc, url, time, query) values (?, ?, ?, ?)",(url,requesturl,timemon,inp.lower()))
        db_global.commit()
        return(url)
    else:
        return(inp+" not found in the Minecraft wiki.")
        
@hook.command
def mcwiki(inp, db_global=None,input=None):
    ",mcwiki <query>/<item id> -- Returns Minecraft wiki search result for <query>/<item id>."
    db_global.execute("create table if not exists mcwiki(desc, url, time, query)")
    db_global.commit()
    if ((inp=="clear cache") and (perm.isowner(input))):
        db_global.execute("DELETE FROM main.`mcwiki`")
        db_global.commit()
        return("cache cleared.")
    timemon = time.strftime("%m", time.gmtime())
    if len(inp)>0:
        requesturl = "http://www.minecraftwiki.net/api.php?format=json&action=query&titles="+inp.replace(" ","%20")+"&prop=revisions&rvprop=content"
        dburl = db_global.execute("select query from mcwiki where query=(?)",(inp.lower(),)).fetchone()
        dbtime = db_global.execute("select time from mcwiki where query=(?)",(inp.lower(),)).fetchone()
        if ((not dburl==None) and (not dbtime==None)):
            (dburl,) = dburl
            (dbtime,) = dbtime
            if ((dbtime==timemon) and (dburl==inp.lower())):
                return dbresponse(inp,requesturl,db_global)
        else:
            url = http.get_json(requesturl)["query"]
            return apiget(inp,url,requesturl,timemon,db_global)