# twitter feed written by Red-M on github or Red_M on esper.net
from util import hook, perm, http
from time import strptime, strftime
import time, json, random, re

def unescape_xml(string):
    return string.replace('&gt;', '>').replace('&lt;', '<').replace('&apos;',
                    "'").replace('&quote;', '"').replace('&amp;', '&')

def get_listid(inp,owner):
    url = 'https://api.twitter.com/1/lists/show.json?slug='+str(inp)+'&owner_screen_name='+str(owner)
    try:
        tweet = http.get_json(url)
        text = (''.join(str(tweet["id"])))
    except http.HTTPError, e:
        return 'error: '+str(e.code)
    
    return(str(text)) 

def errormatch(inp):
    matcher='(error)(:)( )(\\d+)'
    rg = re.compile(matcher,re.IGNORECASE|re.DOTALL)
    m = rg.search(inp)
    if m:
        matches=m.group(1)
        matches+=m.group(2)
        matches+=m.group(3)
        matches+=m.group(4)
        return matches
    else:
        return None
    
def get_twitter(inp):
    try:
        text = 'status/text'
        url = 'http://twitter.com/users/show/%s.xml' % inp
        screen_name = 'screen_name'
        tweet = http.get_xml(url)
        text = unescape_xml(tweet.find(text).text.replace('\n', ''))
        screen_name = tweet.find(screen_name).text
    except http.HTTPError, e:
        return 'error: '+str(e.code)
    return ("@"+str(screen_name)+": "+text.decode('utf-8'))
    
def get_listtwitter(inp):
    try:
        url = 'http://api.twitter.com/1/lists/statuses.json?list_id=%s' % inp
        tweet = http.get_json(url)
        text = unescape_xml(''.join(str(tweet[0]["text"].encode("utf8","replace").replace("\u2026","...").replace("\n",""))))
        screen_name = (''.join(str(tweet[0]["user"]["screen_name"])))
    except http.HTTPError, e:
        return 'error: '+str(e.code)
    return ("@"+str(screen_name)+": "+text.decode('utf-8'))


@hook.command("twitterfeed")
@hook.command
def tfeed(inp, input=None, bot=None, db_global=None):
    "auto tweet getter. ,tfeed <twitter-name-without-@-at-the-start>"
    db_global.execute("create table if not exists twitterfeeds(user, tweet)")
    db_global.commit()
    i=0
    feed = input.inp
    if perm.isadmin(input) and not input.inp=='' and input.conn.conf["rss-on"]==True:
        testss = True
        for xcon in bot.conns:
            if feed not in bot.conns[xcon].conf["twitterfeedchans"]:
                bot.conns[xcon].conf["twitterfeedchans"][feed]=[]
                db_global.execute("insert or replace into twitterfeeds(user, tweet) values (?,?)",(feed, "none"))
            if bot.conns[xcon].conf["twitterfeedchans"][feed].count(bot.conns[xcon].conf["reportchan"])==0:
                bot.conns[xcon].conf["twitterfeedchans"][feed].append(bot.conns[xcon].conf["reportchan"])
        lasttweet = ''.join(db_global.execute("select tweet from twitterfeeds where user=(?)",(feed,)).fetchone())
        input.say("Done. following "+feed)
        ttl=75
        bot.twitterlist[feed]=True
        while testss:
            rss = get_twitter(feed)
            tweet=''.join(rss)
            if lasttweet=='':
                lasttweet="none."
            #print(lasttweet+"\n"+tweet)
            if errormatch(tweet):
                if tweet.endswith("400"):
                    ttl=ttl+60
                    input.say("I have been rate limited on twitter. This means you ether have too many lists/people beening watched at once please ether make a bigger list or remove some of the people/lists being watched...")
                    tweet=lasttweet
                if tweet.endswith("404"):
                    testss= False
                    del bot.twitterlist[feed]
                    return "feed: '"+feed+"' returned: Twitter account by the name of "+feed+" not found."
                if tweet.endswith("500") or tweet.endswith("502") or tweet.endswith("503"):
                    testss= False
                    del bot.twitterlist[feed]
                    return "feed: '"+feed+"' returned: Twitter is down, being upgraded or overloaded. Try again later...."
                else:
                    input.say("feed: '"+feed+"' returned: '"+lasttweet+"'. Something up in here is stuffed....")
                    tweet=lasttweet
                    testss= False
            if lasttweet==tweet and not tweet.startswith("error: "):
                i=i+1
                if i == 32:
                    for xcon in bot.conns:
                        perm.repamsg(input,"No new tweets from '"+feed+"'.")
                    i=0
                time.sleep(ttl)
            elif not lasttweet==tweet and not tweet.startswith("error: "):
                for xcon in bot.conns:
                    for channels in bot.conns[xcon].conf["twitterfeedchans"][feed]:
                        if channels not in bot.conns[xcon].conf["ignore"]:
                            bot.conns[xcon].send('PRIVMSG '+channels+' :TWITTER FEED: '+tweet)
                lasttweet=tweet
                ttl=75
                db_global.execute("delete from twitterfeeds where user=(?)", (feed,)).rowcount
                db_global.execute("insert or replace into twitterfeeds(user, tweet) values (?,?)",(feed, tweet))
                db_global.commit()
                i=0
                time.sleep(ttl)
                testss = True
    else:
        return "Nope."

@hook.command("twitterlistfeed")
@hook.command
def tlfeed(inp, input=None, bot=None, db_global=None):
    "auto twitter list tweet getter. ,tlfeed <twitter-list-name> <owner of list without @ at the start>"
    db_global.execute("create table if not exists twitterlistfeeds(list, tweet)")
    db_global.commit()
    i=0
    check = input.inp.split(' ') 
    feed = str(get_listid(check[0],check[1]))
    feedname = check[0]
    if perm.isadmin(input) and not input.inp=='' and input.conn.conf["rss-on"]==True:
        testss = True
        for xcon in bot.conns:
            if feedname not in bot.conns[xcon].conf["twitterfeedchans"]:
                bot.conns[xcon].conf["twitterfeedchans"][feedname]=[]
                db_global.execute("insert into twitterlistfeeds(list, tweet) values (?,?)",(feedname, "nothing..."))
            if bot.conns[xcon].conf["twitterfeedchans"][feedname].count(bot.conns[xcon].conf["reportchan"])==0:
                bot.conns[xcon].conf["twitterfeedchans"][feedname].append(bot.conns[xcon].conf["reportchan"])
        if db_global.execute("select tweet from twitterlistfeeds where list=(?)",(feedname,)).fetchone()==None:
            lasttweet="nothing..."
        if not db_global.execute("select tweet from twitterlistfeeds where list=(?)",(feedname,)).fetchone()==None:
            lasttweet=''.join(db_global.execute("select tweet from twitterlistfeeds where list=(?)",(feedname,)).fetchone())
        input.say("Done. following "+feedname)
        ttl=75
        bot.twitterlists[feedname]=True
        while testss:
            rss = get_listtwitter(feed)
            tweet=''.join(rss)
            if lasttweet=='':
                lasttweet="none."
            #print(lasttweet+"\n"+tweet)
            if errormatch(tweet):
                if tweet.endswith("400"):
                    ttl=ttl+60
                    return("I have been rate limited on twitter. This means you ether have too many lists/people beening watched at once (the max is 4 without rate limiting from twitter.) please ether make a bigger list or remove some of the people/lists being watched...")
                    tweet=lasttweet
                if tweet.endswith("404"):
                    testss= False
                    del bot.twitterlists[feedname]
                    return "feed: "+feedname+" returned: Twitter list  by the name of "+feedname+" not found made by "+check[1]+"."
                if tweet.endswith("500") or tweet.endswith("502") or tweet.endswith("503"):
                    testss= False
                    del bot.twitterlists[feedname]
                    return "feed: "+feedname+" returned: Twitter is down, being upgraded or overloaded. Try again later...."
                else:
                    input.say("feed: "+feedname+" returned: '"+lasttweet+"'. Something up in here is stuffed....")
                    tweet=lasttweet
                    testss= False
            if lasttweet==tweet and not tweet.startswith("error: "):
                i=i+1
                bot.twitterlists[feedname]=True
                if i == (32):
                    perm.repamsg(input,"No new tweets from '"+feedname+"'.")
                    i=0
                time.sleep(ttl)
            elif not lasttweet==tweet and not tweet.startswith("error: "):
                for xcon in bot.conns:
                    for channels in bot.conns[xcon].conf["twitterfeedchans"][feedname]:
                        bot.conns[xcon].send('PRIVMSG '+channels+' :TWITTER LIST FEED:'+feedname+': '+tweet)
                lasttweet=tweet
                bot.twitterlists[feedname]=True
                db_global.execute("delete from twitterlistfeeds where list=(?)", (feedname,)).rowcount
                db_global.execute("insert or replace into twitterlistfeeds(list, tweet) values (?,?)",(feedname, tweet))
                db_global.commit()
                ttl=75
                i=0
                time.sleep(ttl)
                testss = True
    else:
        return "Nope."

@hook.command("tset")
@hook.command
def twittersettings(inp, input=None, bot=None):
    "This command is for the settings of the auto twitter."
    if perm.isadmin(input) and not input.inp=='':
        check = input.inp.split(' ')
        if len(check)>=2:
            print("twitter channel list cmd:: "+str(check))
            if check[0]=='add' and check[1] and check[1]:
                if input.conn.conf["twitterfeedchans"][check[1]].count(check[2])==0:
                    if check[2].startswith("#"):
                        input.conn.conf["twitterfeedchans"][check[1]].append(check[2])
                        input.conn.conf["twitterfeedchans"][check[1]].sort()
                        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=1)
                        return("done.")
                    else:
                        return(check[2]+" is not a channel! only channels can be added to a twitter feed's channel list!")
                elif input.conn.conf["twitterfeedchans"][check[1]].count(check[2])==1:
                    return("Nope."+check[2]+" is already on "+check[1]+"'s channels list!")
            if check[0]=='add' and (not check[1] or not check[2]):
                return("invalid syntax. please try again with ,twitterchan "+check[0]+" <twitter account> <#channel to add>")
            if check[0]=='del' or check[0]=='delete' and check[1] and check[2]:
                if input.conn.conf["twitterfeedchans"][check[1]].count(str(check[2]))==1:
                    if check[2].startswith("#"):
                        input.conn.conf["twitterfeedchans"][check[1]].remove(check[2])
                        input.conn.conf["twitterfeedchans"][check[1]].sort()
                        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=1)
                        return("done.")
                    else:
                        return(check[2]+" is not a channel! only channels can be removed from a twitter feed's channel list!")
                else:
                    return("Nope."+check[2]+" is not on "+check[1]+"'s channels list!")
            if check[0]=='del' or check[0]=='delete' and (not check[1] or not check[2]):
                return("invalid syntax. please try again with ,twitterchan "+check[0]+" <twitter account> <#channel to remove>")
            if check[0]=='list' and check[1] and not check[1]=='all':
                tchan={}
                for xcon in bot.conns:
                    tchan[xcon]=[]
                    for channels in bot.conns[xcon].conf["twitterfeedchans"][check[1]]:
                        tchan[xcon].append(channels)
                return("channels that will recieve '"+check[1]+"''s tweets are: "+(str(dict(tchan)).replace("{u'","").replace("u'","").replace("[","").replace("]","").replace("}","").replace("'","")))
            if check[0]=='list' and check[1] and check[1]=='all':
                tchan={}
                for xcon in bot.conns:
                    tchan[xcon]=[]
                    for users in bot.conns[xcon].conf["twitterfeedchans"]:
                        tchan[xcon].append(users)
                return("I am watching these twitter accounts for any new tweets: "+(str(dict(tchan)).replace("{u'","").replace("u'","").replace("[","").replace("]","").replace("}","").replace("'","")))
            if check[0]=='list' and not check[1]:
                return("invalid syntax. please try again with ,twitterchan "+check[0]+" <twitter account>")
            else:
                return("Command not recognised '"+check[0]+"' valid commands for this cmd are : 'add', 'del'/'delete' and 'list'. So replace "+check[0]+" with one of these commands!")
        else:
            return("invalid syntax. please try again with ,twitterchan <add,del/delete,list> <twitter account> [#channel]")

            
@hook.command
def twitterlistid(inp, input=None):
    check = input.inp.split(' ')
    out = get_listid(check[0], check[1])
    return out