# -*- coding: utf-8 -*-
# SCP Foundation wiki scrapper made by Red_M on esper.net or Red-M on GitHub.com
# used parts of the google search plugin to get our scp wiki url
# used parts of the page titler to obtain some info
from util import hook, http, urlnorm
import urllib
import httplib
import urllib2
import re
import time
import urlparse
import repaste
import urlhistory

ignored_urls = ["http://youtube.com"]
wordDic = {
'<p>': '',
'</p>': '',
'<strong>': '\x02',
'</strong>': '\x02'
}

def check_response(headers):
    type = headers.get("content-type", None)
    if not type or "html" not in type:
        reply = "Link is not HTML but %s" % type
        length = headers.get("content-length", None)
        if length is not None:
            reply += ", length %s" % length
        lastmodified = headers.get("last-modified", None)
        if lastmodified is not None:
            reply += ", last modified %s " % lastmodified
        return reply

def multiwordReplace(text, wordDic):
    rc = re.compile('|'.join(map(re.escape, wordDic)))
    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)

def page(inp,host): #gets our SCP url from the first google search result. this allows for queries instead of just SCP item ids.
    url = 'http://ajax.googleapis.com/ajax/services/search/web?q='+str("site:scp-wiki.net "+inp).replace(" ","%20")+'&v=1.0&safe=off&client=google-csbe&userip='+host
    parsed = http.get_json(url)
    #print(url)
    if not parsed['responseStatus']==200:
        raise IOError('error searching for pages: %s' % (parsed['responseStatus']))
    if not parsed['responseData']['results']:
        return 'No results found.'
    result = parsed['responseData']['results'][0]
    title = http.unescape(result['titleNoFormatting'])
    content = http.unescape(result['content'])
    if len(content) == 0:
        content = "No description available."
    else:
        content = http.html.fromstring(content).text_content()
    out = '%s' % (result['unescapedUrl'])
    out = ' '.join(out.split())
    return out
    
def parse(match,titler): #parser for getting data of any SCP
    url = urlnorm.normalize(match.encode('utf-8'))
    if url not in ignored_urls:
        url = url.decode('utf-8')
        try:
            parts = urlparse.urlsplit(url)
            conn = httplib.HTTPConnection(parts.hostname, timeout=10)
            path = parts.path
            if parts.query:
                path += "?" + parts.query
            conn.request('HEAD', path)
            resp = conn.getresponse()
            if not (200 <= resp.status < 400):
                return "Error: HEAD %s %s " % (resp.status, resp.reason)
            errors = check_response(dict(resp.getheaders()))
            if errors:
                return errors
        except Exception as e:
            return "Error: " + str(e)
        try:
            req = urllib2.urlopen(url)
        except Exception as e:
            return "Error: GET %s " % e
        errors = check_response(req.headers)
        if errors:
            return errors
        text = req.read().decode('utf8', 'ignore').replace("\n","")
        match = titler.search(text)
        if not match:
            return "Error: no title 1"
        rawtitle = match.group(1)
        mat2 = match.group(2)
        mat3 = match.group(3)
        title = repaste.decode_html(rawtitle)
        title = " ".join(title.split())
        ret = (title,mat2,mat3)
        return ret
        
def dbresponse(url,db_global):
    (itemname, itemid, classtype, desc, url, timemon) = db_global.execute("select itemname, itemid, classtype, desc, url, time from scpwiki where url=(?)",(url,)).fetchone()
    for dart in wordDic:
        desc = desc.replace(dart,wordDic[dart])
    for dart in wordDic:
        itemname = itemname.replace(dart,wordDic[dart])
    for dart in wordDic:
        itemid = itemid.replace(dart,wordDic[dart]).replace("SCP-","").replace("scp-","")
    for dart in wordDic:
        classtype = classtype.replace(dart,wordDic[dart])
    return("Item Name:\x02\x1f"+itemname+"\x02\x1f Item #:\x02\x1f"+itemid+"\x1f\x02 Class:'\x02\x1f"+classtype+"\x1f\x02'. "+desc)
        
def goturlforscp(url,scpid,db_global,timemon):
    scpid = url.replace("http://www.scp-wiki.net/scp-","") #gets scpid as string
    if scpid.endswith("-j"):
        iscpid = int(scpid.replace("-j",""))
    if not scpid.endswith("-j"):
        iscpid = int(scpid) #lets see if we can get it as a int for range testing
    if type(iscpid)==type(1):
        if not scpid.endswith("-j") and iscpid in range(1,1000): #item name url to get our SCP's item name from
            urltitle = "http://www.scp-wiki.net/scp-series"
        if not scpid.endswith("-j") and iscpid in range(1000,2000):
            urltitle = "http://www.scp-wiki.net/scp-series-2"
    titler = re.compile(r'.*Item #:(.+?)Object Class:(.+?)Special Containment Procedures:.*?Description:(.+?)</p>')
    title = parse(url,titler)#.replace("</p>","").replace("<p>","") #^- regex to get the data we want. <- passes the url and regex to the parser
    if type(title)==type(("","")): #check to see if we get an error from our parser
        (itemid,classtype,desc) = title
    if not type(title)==type(("","")):
        (itemid,classtype,desc) = ("","","") #if we get an error then set our other values to nothing
    if not scpid.endswith("-j"): #checking if we have a joke SCP
        itemname = parse2(urltitle,re.compile('.*<li><a href="/scp-'+str(iscpid)+'">SCP-'+str(iscpid)+'</a> - (.+?)</li>.*')) #if we dont then lets get the item name
    if scpid.endswith("-j"):
        itemname = "" #if we do then lets not show an item name as we cant get one
    db_global.execute("insert or replace into scpwiki(itemname, itemid, classtype, desc, url, time) values (?, ?, ?, ?, ?, ?)",(itemname,itemid,classtype,desc,url,timemon))
    db_global.commit()
    return("Item Name:\x02\x1f"+itemname+"\x02\x1f Item #:\x02\x1f"+itemid+"\x1f\x02 Class:'\x02\x1f"+classtype+"\x1f\x02'. "+desc)
        
@hook.command
def scp(inp, db_global=None,input=None):
    ",scp <query>/<item id> -- Returns SCP Foundation wiki search result for <query>/<item id>."
    db_global.execute("create table if not exists scpwiki(itemname, itemid, classtype, desc, url, time)")
    db_global.commit()
    timemon = time.strftime("%m", time.gmtime())
    if len(inp)>3:
        url = page(inp,input.host)
        inten = 0 #string testing
    if len(inp)==3:
        url = page(inp,input.host)
        inten = 1 #int testing for an scp item id
    if len(inp)==2:
        url = page("0"+inp,input.host)
        inten = 1
    if len(inp)==1:
        url = page("00"+inp,input.host)
        inten = 1
    if not inten==1:
        url = page(inp,input.host)
    dburl = db_global.execute("select url from scpwiki where url=(?)",(url,)).fetchone()
    if not dburl==None:
        return dbresponse(url,db_global)
    else:
        scpid = url.replace("http://www.scp-wiki.net/scp-","")
        url = "http://www.scp-wiki.net/scp-"+scpid
        return goturlforscp(url,scpid,db_global,timemon)

def parse2(match,titler2): #parser for the item name. this will be skipped if we have a joke SCP
    url = urlnorm.normalize(match.encode('utf-8'))
    if url not in ignored_urls:
        url = url.decode('utf-8')
        try:
            parts = urlparse.urlsplit(url)
            conn = httplib.HTTPConnection(parts.hostname, timeout=10)
            path = parts.path
            if parts.query:
                path += "?" + parts.query
            conn.request('HEAD', path)
            resp = conn.getresponse()
            if not (200 <= resp.status < 400):
                return "Error: HEAD %s %s " % (resp.status, resp.reason)
            errors = check_response(dict(resp.getheaders()))
            if errors:
                return errors
        except Exception as e:
            return "Error: " + str(e)
        try:
            req = urllib2.urlopen(url)
        except Exception as e:
            return "Error: GET %s " % e
        errors = check_response(req.headers)
        if errors:
            return errors
        text = req.read().decode('utf8', 'ignore').replace("\n","")
        match = titler2.search(text)
        if not match:
            return "Error: no title 2"
        rawtitle = match.group(1)
        title = repaste.decode_html(rawtitle)
        title = " ".join(title.split())
        return title