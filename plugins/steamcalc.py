from util import hook, http
import re

count_re = re.compile(r"Found (.*?) Games with a value of ")


@hook.command
def steamcalc(inp):
    "uses steamcalculator.com to find out how much a steam account is worth. doesnt do DLC."
    if " " in inp:
        return "Invalid Steam ID"

    url = "http://www.steamcalculator.com/id/{}".format(http.quote_plus(inp))

    try:
        page = http.get_html(url)
    except Exception as e:
        return "Could not get Steam game listing: {}".format(e)

    try:
        count = page.xpath("//div[@id='rightdetail']/text()")[0]
        number = count_re.findall(count)[0]

        value = page.xpath("//div[@id='rightdetail']/h1/text()")[0]
    except:
        return("Steam account not found under: "+inp)

    #short_url = web.isgd(url)

    return "Found {} games with a value of {}!".format(number, value)
