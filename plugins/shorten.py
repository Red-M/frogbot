# Plugin by Lukeroge 
# <lukeroge@gmail.com> <https://github.com/lukeroge/CloudBot/>

from util import hook, http
from re import match
from urllib2 import urlopen, Request, HTTPError
from urllib import urlencode

class ShortenError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def bitly(url, user, apikey):
    try:
        if url[:8] == "https://":
            pass
        elif url[:7] != "http://":
            url = "http://" + url
        params = urlencode({'longUrl': url, 'login': user, 'apiKey': apikey, 'format': 'json'})
        j = http.get_json("http://api.bit.ly/v3/shorten?%s" % params)
        if j['status_code'] == 200:
            return j['data']['url']
        raise ShortenError('%s' % j['status_txt'])
    except (HTTPError, ShortenError):
        return "Could not shorten %s!" % url

@hook.command
def shorten(inp, bot = None):
    ".shorten <url> - Makes an j.mp/bit.ly shortlink to the url provided."
    api_user = bot.config.get("api_keys", {}).get("bitly_user", None)
    api_key = bot.config.get("api_keys", {}).get("bitly_api", None)
    if api_key is None:
        return "error: no api key set"
    return bitly(inp, api_user, api_key)

def adflyss(url, user, apikey):
    try:
        if url[:8] == "https://":
            url = "https://" + url
        elif url[:7] != "http://":
            url = "http://" + url
        params = urlencode({'key': apikey, 'uid': user, 'advert_type': 'int', 'domain': 'adf.ly', 'url': url, 'format': 'json'})
        return str(http.get("http://api.adf.ly/api.php?%s" % params))
    except (HTTPError, ShortenError):
        return "Could not shorten %s!" % url

@hook.command
def adfly(inp, bot = None):
    ".adfly <url> - Makes an adf.ly shortlink to the url provided."
    api_user = bot.config.get("api_keys", {}).get("adfly_usernumber", None)
    api_key = bot.config.get("api_keys", {}).get("adfly_api", None)
    if api_key is None:
        return "error: no api key set"
    return adflyss(inp, api_user, api_key)

@hook.command
def expand(inp, bot = None):
    ".expand <url> - Gets the original URL from a shortened link."
    try:
        url = http.get_url(inp)
    except HTTPError, e:
        return "Failed to expand URL."
    return url
