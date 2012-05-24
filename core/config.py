import inspect
import json
import os


def save(conf):
    json.dump(conf, open('config', 'w'), sort_keys=True, indent=2)

if not os.path.exists('config'):
    open('config', 'w').write(inspect.cleandoc(
        r'''
        {
          "connections":
          {
            "local irc":
            {
              "user": "frogbot",
              "realname": "frogbot",
              "server": "localhost",
              "nick": "MyNewFrogBot",
              "channels": ["#test"],
              "admins": ["Red_M"],
              "superadmins": ["Red_M"],
              "owner": ["Red_M"],
              "reportchan": "#frog",
              "restartcmd": "bot.py",
              "bots": [],
              "ftp_host": "",
              "ftp_port": 21,
              "ftp_user": "",
              "ftp_pw": "",
              "ftp_dir": "",
              "ignore": [],
              "twitterfeedchans": ["local irc":[]],
              "rss-on": "True"
            }
          },
          "disabled_plugins": [],
          "disabled_commands": [],
          "acls": {},
          "api_keys": 
          {
            "geoip": "INSERT API KEY FROM ipinfodb.com HERE",
            "tvdb": "INSERT API KEY FROM thetvdb.com HERE",
            "bitly_user": "INSERT USERNAME FROM bitly.com HERE",
            "bitly_api": "INSERT API KEY FROM bitly.com HERE",
            "adfly_usernumber": "INSERT USER NUMBER KEY FROM adf.ly HERE",
            "adfly_api": "INSERT API KEY FROM adf.ly HERE",
            "wolframalpha": "INSERT API KEY FROM wolframalpha.com HERE",
            "lastfm": "INSERT API KEY FROM lastfm HERE",
            "mc_user": "INSERT MINECRAFT USERNAME HERE",
            "mc_pass": "INSERT MINECRAFT PASSWORD HERE",
			"google": "INSERT API KEY FROM GOOGLE.COM HERE"
          },
          "log": "true",
          "censored_strings":
          [
            "DCC SEND",
            "1nj3ct",
            "thewrestlinggame",
            "startkeylogger",
            "hybux",
            "\\0",
            "\\x01",
            "!coz",
            "!tell /x"
          ]
        }''') + '\n')


def config():
    # reload config from file if file has changed
    config_mtime = os.stat('config').st_mtime
    if bot._config_mtime != config_mtime:
        try:
            bot.config = json.load(open('config'))
            bot._config_mtime = config_mtime
        except ValueError, e:
            print 'ERROR: malformed config!', e


bot._config_mtime = 0
