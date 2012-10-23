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
    
def dataget(url,wikiurl,wikilen):
    pageid = url['pages'].keys()[0]
    name = url['pages'][pageid][u'title']
    url = url['pages'][pageid][u'revisions'][0]['*'].replace("\n","")
    if url.startswith("#REDIRECT "):
        return url
    textb = {}
    textb[regexmatch2(url,re.compile(r'.+?(\|sounds=.+?\}\}'+'\n\n'+')',re.DOTALL))] = ""
    page = http.get_html(wikiurl+name)
    for p in page.xpath('//div[@class="mw-content-ltr"]/p'):
        if p.text_content():
            plen = len(p.text_content())
            if plen>=wikilen:
                summary = " ".join(p.text_content().splitlines())
                summary = re.sub("\[\d+\]", "", summary)
                summary = text.truncate_str(summary, 250)
                return ("%s :: \x02%s\x02" % (summary, wikiurl+name)).encode('utf8')[:400]

    return "Unknown Error."
    
def apiget(inp,url,requesturl,timemon,db_global,wiki,wikiname,wikiurl,wikilen):
    pageid = url['pages'].keys()[0]
    if not pageid=="-1":
        url = dataget(url,wikiurl,wikilen)
        for dart in wordDic2:
            url = url.replace(dart,wordDic2[dart])
        while url.startswith("#REDIRECT "):
            url2 = http.get_json("http://www."+wiki+"wiki.net/api.php?format=json&action=query&titles="+url.replace("#REDIRECT ","").replace(" ","%20")+"&prop=revisions&rvprop=content")["query"]
            url = dataget(url2,wikiurl,wikilen)
        db_global.execute("insert or replace into "+wikiname+"wiki(desc, url, time, query) values (?, ?, ?, ?)",(url,requesturl,timemon,inp.lower()))
        db_global.commit()
        return(url)
    else:
        return(inp+" not found in the "+wiki+" wiki.")

def wikia(inp,input,db_global,wiki,wikiname,wikiurl,wikilen,wikiwiki):
    db_global.execute("create table if not exists "+wikiname+"wiki(desc, url, time, query)")
    db_global.commit()
    if ((inp=="clear cache") and (perm.isowner(input))):
        db_global.execute("DELETE FROM main.`"+wikiname+"wiki`")
        db_global.commit()
        return("cache cleared.")
    timemon = time.strftime("%m", time.gmtime())
    if len(inp)>0:
        requesturl = wikiwiki+"api.php?format=json&action=query&titles="+inp.replace(" ","%20")+"&prop=revisions&rvprop=content"
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
        
@hook.command("mcwiki")
@hook.command
def minecraftwiki(inp, db_global=None,input=None):
    ",mcwiki <query> -- Returns Minecraft wiki search result for <query>."
    wikiname = "mc"
    wiki = "minecraft"
    wikilen = 1
    wikiurl = "http://www."+wiki+"wiki.net/wiki/"
    wikiwiki = "http://www."+wiki+"wiki.net/"
    return(wikia(inp,input,db_global,wiki,wikiname,wikiurl,wikilen,wikiwiki))
    