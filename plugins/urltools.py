from util import hook, http, urlnorm, perm
import urllib
import httplib
import urllib2
import re
import urlparse
import repaste
import urlhistory

ignored_urls = ["http://youtube.com","https://youtube.com","https://www.youtube.com","http://www.youtube.com","http://pastebin.com","http://www.pastebin.com","http://mibpaste.com","http://fpaste.com"]
maxlen = 4086
titler = re.compile(r'(?si)<title>(.+?)</title>')
wordDic = {
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
'  ': ' '}

def check_response(headers):
    type = headers.get("content-type", None)
    if not type or "html" not in type:
        reply = "%s" % type
        length = headers.get("content-length", None)
        if length is not None:
            reply += ", length %s" % length
        lastmodified = headers.get("last-modified", None)
        if lastmodified is not None:
            reply += ", last modified %s " % lastmodified
        return reply

def parse(match):
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
        text = req.read(maxlen).decode('utf8', 'ignore')
        match = titler.search(text)
        if not match:
            return "Error: no title "
        rawtitle = match.group(1)
        title = repaste.decode_html(rawtitle)
        title = " ".join(title.split())
        return title

def multiwordReplace(text, wordDic):
    rc = re.compile('|'.join(map(re.escape, wordDic)))
    def translate(match):
        return wordDic[match.group(0)]
    return rc.sub(translate, text)

from urllib import urlencode

class ShortenError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def isgd(inp):
    data = urllib.urlencode(dict(format="simple", url=inp))

    try:
        return urllib2.urlopen("http://is.gd/create.php", data).read()
    except Exception as e:
        return "Error: %s" % e

    return shortened
        
def urltest(url,match):
    if not type(url) is type("i"):
        return urlnorm.normalize(match.group().group("id").encode('utf-8'))
    else:
        return ""

@hook.regex(r'((?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~\/|\/)?P<id>?(?#Username:Password)(?:\w+:\w+@)?(?#Subdomains)(?:(?:[-\w]+\.)+(?#TopLevel Domains)(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2}))(?#Port)(?::[\d]{1,5})?(?#Directories)(?:(?:(?:\/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|\/)+|\?|#)?(?#Query)(?:(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=?(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*)*(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?$|([a-zA-Z]+://|www\.)[^ ]+)')
def urlparser(match, say = None, input=None, bot=None):
    inpo = input.params.replace(input.chan+" :","")
    url = urlnorm.normalize(match.group().encode('utf-8'))
    url2 = urltest(url,match)
    if (not input.conn.conf['autotitle']==False) and (not (perm.isignored(input) or perm.isbot(input))) and not (inpo.startswith(",t") or inpo.startswith(",title") or inpo.startswith(",shor")) and not ("@" in url):
        #print "[debug] URL found"
        if not (url.startswith("http://") or url.startswith("https://") or url.startswith("ftp://")):
            url = "http://"+url
        for x in ignored_urls:
            if x in url:
                return
        title = parse(url)
        if title == "fail":
            print "[url] No title found"
            return("(Link) No title found")
        title = multiwordReplace(title, wordDic)
        realurl = http.get_url(url)
        api_user = bot.config.get("api_keys", {}).get("bitly_user", None)
        api_key = bot.config.get("api_keys", {}).get("bitly_api", None)
        if api_key is None:
            return "error: no api key set"
        realurl = isgd(realurl)
        if realurl == url:
            return("(Link) %s" % title)
        else:
            return("(Link) %s <=> %s" % (realurl, title))
    else:
        return
