from util import hook, http
import urlhistory
import httplib
import re
import urlparse
import urllib2
import repaste


maxlen = 4086
titler = re.compile(r'(?si)<title>(.+?)</title>')


@hook.regex(r".*(cobaltforum\.net/viewtopic\.php\?[\w=&]+)\b.*")
def regex(inp, say=None):
    "titles minecraftforum urls"
    t = title("http://" + inp.group(1)).replace(" - Minecraft Forums", "")
    if t == "Login":
        return
    say("mcforum title: " + t)


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


@hook.command
@hook.command("t")
def title(inp, db=None, chan=None):
    ".title <url> - get title of <url>"
    if inp == '^':
        urlhistory.db_init(db)
        rows = db.execute("select url from urlhistory where chan = ? order by time desc limit 1", (chan,))
        if not rows.rowcount:
            return "No url in history."

        inp = rows.fetchone()[0]

    try:
        parts = urlparse.urlsplit(inp)
        conn = httplib.HTTPConnection(parts.hostname, timeout=10)
        path = parts.path

        if parts.query:
            path += "?" + parts.query

        conn.request('HEAD', path)
        resp = conn.getresponse()

        if not (200 <= resp.status < 400):
            return "Error: HEAD %s %s" % (resp.status, resp.reason)

        errors = check_response(dict(resp.getheaders()))

        if errors:
            return errors
    except Exception as e:
        return "Error: " + str(e)

    try:
        req = urllib2.urlopen(inp)
    except Exception as e:
        return "Error: GET %s" % e

    errors = check_response(req.headers)

    if errors:
        return errors

    text = req.read(maxlen).decode('utf8', 'ignore')

    match = titler.search(text)

    if not match:
        return "Error: no title"

    rawtitle = match.group(1)

    title = repaste.decode_html(rawtitle)
    title = " ".join(title.split())

    return title
