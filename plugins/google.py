import random
from util import hook
from util import http

@hook.command('image')
@hook.command('gis')
@hook.command
def googleimage(inp):
    ".gis <term> -- Returns first Google Image result (Safesearch off)."
    if '^' in inp:
        inp = str(inp).replace("^", bot.chanseen[input.conn.server][input.chan][0])
    url = 'http://ajax.googleapis.com/ajax/services/search/images?q='+str(inp).replace(" ","%20")+'&v=1.0&safe=off'
    parsed = http.get_json(url)
    if not 200 <= parsed['responseStatus'] < 300:
        raise IOError('error searching for images: %d: %s' % ( \
                      parsed['responseStatus'], ''))
    if not parsed['responseData']['results']:
        return 'no images found'
    return random.choice(parsed['responseData']['results'][:10])\
                        + ['unescapedUrl']


@hook.command('search')
@hook.command('g')
@hook.command
def google(inp):
    ".google <query> -- Returns first google search result for <query>."
    url = 'http://ajax.googleapis.com/ajax/services/search/web?q='+str(inp).replace(" ","%20")+'&v=1.0&safe=off&client=google-csbe'
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
    out = '%s -- \x02%s\x02: "%s"' % (result['unescapedUrl'], title, content)
    out = ' '.join(out.split())
    if len(out) > 300:
        out = out[:out.rfind(' ')] + '...'
    return out