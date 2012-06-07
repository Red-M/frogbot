import re
from util import hook, http, misc

@hook.command
def calc(inp):
    "calc <term> -- Calculate <term> with Google Calc."
    page = http.get('http://www.google.com/search?q='+inp.replace("+","%2B").replace("/","%2F"))
    rrg = re.compile('.*doctype html>(.*)<h2 class="r" dir="ltr" style="font-size:138%">.*')
    rep = rrg.findall(page)
    rrrg = re.compile('.*<div style="padding-top:5px">(.*)</html>')
    rrep = rrrg.findall(page)
    rep.append(''.join(rrep))
    for data in rep:
        page = page.replace(data,"")
    #print "\n\n"+page
    rg = re.compile('.*<h2 class="r" dir="ltr" style="font-size:138%">(.*)</h2>')
    m = rg.match(page)
    if m is None:
        return "could not calculate " + inp
    result = m.group(1).replace("<font size=-2> </font>", ",").replace(" &#215; 10<sup>", "E").replace("</sup>", "").replace("\xa0", ",").decode("utf8")
    return result