# -*- coding: utf-8 -*-
# wikia scrapper made by Red_M on esper.net or Red-M on GitHub.com
# direct clone of the minecraft wiki scrapper but for wikia
# used parts of the SCP wiki scrapper to build this one...
from util import hook, http, urlnorm, perm, text
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
    
def dbresponse(query,url,db_global,wikiname):
    (desc, url, timemon, query) = db_global.execute("select desc, url, time, query from "+wikiname+"wiki where query=(?)",(query.lower(),)).fetchone()
    return("(Cached) "+desc)
    
def dataget(url,wikiurl,wikilen,recur):
    pageid = url['pages'].keys()[0]
    name = url['pages'][pageid][u'title']
    if "revisions" in url['pages'][pageid].keys():
        url = url['pages'][pageid]['revisions'][0]['*'].replace("\n","")[:400]
        if url.startswith("#REDIRECT "):
            recur+=1
            return url.replace("[","").replace("]",""),recur
        textb = {}
        textb[regexmatch2(url,re.compile(r'.+?(\|sounds=.+?\}\}'+'\n\n'+')',re.DOTALL))] = ""
    page = http.get_html(wikiurl+name.replace(" ","%20"))
    for p in page.xpath('//div[@class="mw-content-ltr"]/p'):
        if p.text_content():
            plen = len(p.text_content())
            if plen>=wikilen:
                summary = " ".join(p.text_content().splitlines())
                summary = re.sub("\[\d+\]", "", summary)
                summary = text.truncate_str(summary, 250)
                return ("%s :: \x02%s\x02" % (summary, wikiurl+name)).encode('utf8')[:400],recur

    return "Unknown Error."
    
def apiget(inp,url,requesturl,timemon,db_global,wiki,wikiname,wikiurl,wikilen):
    pageid = url['pages'].keys()[0]
    if not pageid=="-1":
        (url,i) = dataget(url,wikiurl,wikilen,0)
        for dart in wordDic2:
            url = url.replace(dart,wordDic2[dart])
        while url.startswith("#REDIRECT "):
            url2 = http.get_json("http://www."+wiki+".wikia.com/api.php?format=json&action=query&titles="+url.replace("#REDIRECT ","").replace("[","").replace("]","").replace(" ","%20")+"&prop=revisions&rvprop=content")["query"]
            (url,i) = dataget(url2,wikiurl,wikilen,i)
        db_global.execute("insert or replace into "+wikiname+"wiki(desc, url, time, query) values (?, ?, ?, ?)",(url,requesturl,timemon,inp.lower()))
        db_global.commit()
        return(url)
    else:
        return(inp+" not found in the "+wiki+" wiki.")

def wikia(inp,input,db_global,wiki,wikiname,wikiurl,wikilen):
    db_global.execute("create table if not exists "+wikiname+"wiki(desc, url, time, query)")
    db_global.commit()
    if ((inp=="clear cache") and (perm.isowner(input))):
        db_global.execute("DELETE FROM main.`"+wikiname+"wiki`")
        db_global.commit()
        return("cache cleared.")
    timemon = time.strftime("%m", time.gmtime())
    if len(inp)>0:
        requesturl = "http://www."+wiki+".wikia.com/api.php?format=json&action=query&titles="+inp.replace(" ","%20")+"&prop=revisions&rvprop=content"
        dburl = db_global.execute("select query from "+wikiname+"wiki where query=(?)",(inp.lower(),)).fetchone()
        dbtime = db_global.execute("select time from "+wikiname+"wiki where query=(?)",(inp.lower(),)).fetchone()
        if ((not dburl==None) and (not dbtime==None)):
            (dburl,) = dburl
            (dbtime,) = dbtime
            if ((dbtime==timemon) and (dburl==inp.lower())):
                return dbresponse(inp,requesturl,db_global,wikiname).encode("utf8")
        else:
            url = http.get_json(requesturl)["query"]
            return apiget(inp,url,requesturl,timemon,db_global,wiki,wikiname,wikiurl,wikilen).encode("utf8")
        
@hook.command
def mlpwiki(inp, db_global=None,input=None):
    ",mlpwiki <query> -- Returns MLP wikia search result for <query>."
    wikiname = "mlp"
    wiki = "mlp"
    wikilen = 1
    wikiurl = "http://"+wiki+".wikia.com/wiki/"
    return(wikia(inp,input,db_global,wiki,wikiname,wikiurl,wikilen))

@hook.command("mncwiki")
@hook.command("smncwiki")
@hook.command
def mondaynightcombatwiki(inp, db_global=None,input=None):
    ",mondaynightcombatwiki <query> -- searches the MNC/SMNC wiki for <query>"
    wikiname = "MNC"
    wiki = "mondaynightcombat"
    wikilen = 60
    wikiurl = "http://"+wiki+".wikia.com/wiki/"
    return(wikia(inp,input,db_global,wiki,wikiname,wikiurl,wikilen))

@hook.command("ddwiki")
@hook.command
def dungeondefenderswiki(inp, db_global=None,input=None):
    ",dungeondefenderswiki <query> -- Returns dungeon defenders wikia search result for <query>."
    wikiname = "dd"
    wiki = "dungeondefenders"
    wikilen = 30
    return(wikia(inp,input,db_global,wiki,wikiname,wikiurl,wikilen))
    
@hook.command("gowwiki")
@hook.command
def gearsofwarwiki(inp, db_global=None,input=None):
    ",gearsofwarwiki <query> -- Returns Gears of war wikia search result for <query>."
    wikiname = "gow"
    wiki = "gearsofwar"
    wikiurl = "http://"+wiki+".wikia.com/wiki/"
    wikilen = 30
    return(wikia(inp,input,db_global,wiki,wikiname,wikiurl,wikilen))
    
@hook.command
def halowiki(inp, db_global=None,input=None):
    ",halowiki <query> -- Returns Halo wikia search result for <query>."
    wikiname = "halo"
    wiki = "halo"
    wikilen = 30
    wikiurl = "http://"+wiki+".wikia.com/wiki/"
    return(wikia(inp,input,db_global,wiki,wikiname,wikiurl,wikilen))
    
@hook.command("pdwiki")
@hook.command
def paydaywiki(inp, db_global=None,input=None):
    ",paydaywiki <query> -- Returns Payday: The heist wikia search result for <query>."
    wikiname = "pd"
    wiki = "payday"
    wikilen = 30
    wikiurl = "http://"+wiki+".wikia.com/wiki/"
    return(wikia(inp,input,db_global,wiki,wikiname,wikiurl,wikilen))
    
