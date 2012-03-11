from util import hook, http
import urllib
import urllib2
import httplib
import time
import urlparse
import re

re_adfly = re.compile(r'var url = \'([^\']+)\'')


@hook.command
def isgd(inp):
    ".isgd <url> -- shorten link using is.gd"

    data = urllib.urlencode(dict(format="simple", url=inp))

    try:
        return urllib2.urlopen("http://is.gd/create.php", data).read()
    except Exception as e:
        return "Error: %s" % e

    return shortened


@hook.command
def expand(inp):
    ".expand <shorturl> -- expand link shortened url"

    # try HEAD
    parts = urlparse.urlsplit(inp)
    conn = httplib.HTTPConnection(parts.hostname)
    path = parts.path
    if parts.query:
        path += "?" + parts.query
    conn.request('HEAD', path)
    resp = conn.getresponse()
    location = resp.msg.getheader("Location")

    if not location:
        return inp

    expandedparts = urlparse.urlsplit(location)
    quoted = expandedparts._replace(path=urllib.quote(expandedparts.path))
    url = quoted.geturl()

    return url


def db_init(db):
    db.execute("create table if not exists deadfly_cache (adfly primary key, url)")
    db.commit()


def db_get(db, adfly):
    return db.execute("select url from deadfly_cache where adfly = ?", (adfly, )).fetchone()


def db_add(db, adfly, url):
    db.execute("insert into deadfly_cache (adfly, url) values (?,?)", (adfly, url))
    db.commit()


@hook.command
def deadfly(inp, db=None):
    ".deadfly <adf.ly url> -- scrapes link shortened by adf.ly"
    db_init(db)

    result = db_get(db, inp)

    if result:
        return result[0]

    parts = urlparse.urlsplit(inp)

    parts = parts._replace(netloc=parts.netloc + ".nyud.net")
    url = urlparse.urlunsplit(parts)
    timeout = 15

    try:
        text = urllib2.urlopen(url, timeout=timeout).read()
    except Exception, e:
        print e
        url = inp
        try:
            text = urllib2.urlopen(url, timeout=timeout).read()
        except Exception, e:
            print e
            return "Error"

    result = re_adfly.search(text).group(1)

    db_add(db, inp, result)

    return result
