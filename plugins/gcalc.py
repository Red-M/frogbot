import re
from util import hook, http, misc

@hook.command
def calc(inp):
    "calc <term> -- Calculate <term> with Google Calc."
    page = http.get('http://www.google.com/search?q='+inp.replace("+","%2B").replace("/","%2F").replace(" ","%20"))
    #print "\n\n"+page
    rg = re.compile('.*<div class=\"cwtlotc\"> <span class=\"cwcot\" id=\"cwos\"> (.+?)  </span> </div> <div class=\"cwtlptc\">.*')
    m = rg.findall(page)
    if (m is None) or (len(m)==0):
        return "could not calculate " + inp
    result = inp+' '+m[0].replace("<font size=-2> </font>", ",").replace(" &#215; 10<sup>", "E").replace("</sup>", "").replace("\xa0", ",").decode("utf8")
    return result