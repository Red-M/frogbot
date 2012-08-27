import inspect
import json
import os


def save(conf):
    json.dump(conf, open('config', 'w'), sort_keys=True, indent=1)

if not os.path.exists('config'):
    open('config', 'w').write(inspect.cleandoc(
r'''{
 "acls": {}, 
 "api_keys": {
  "adfly_api": "INSERT API KEY FROM adf.ly HERE", 
  "adfly_usernumber": "INSERT ACCOUNT NUMBER FROM adf.ly HERE", 
  "bitly_api": "INSERT API KEY FROM bit.ly HERE", 
  "bitly_user": "INSERT USERNAME FROM bit.ly HERE", 
  "geoip": "INSERT API KEY FROM ipinfodb.com HERE", 
  "google": "INSERT API KEY FROM google.com HERE", 
  "lastfm": "INSERT API KEY FROM lastfm HERE", 
  "mc_pass": "INSERT MINECRAFT PASSWORD HERE", 
  "mc_user": "INSERT MINECRAFT USERNAME HERE", 
  "tvdb": "INSERT API KEY FROM thetvdb.com HERE", 
  "wolframalpha": "INSERT API KEY FROM wolframalpha.com HERE"
 }, 
 "censored_strings": [
  "DCC SEND", 
  "1nj3ct", 
  "thewrestlinggame", 
  "startkeylogger", 
  "hybux", 
  "\\0", 
  "\\x01", 
  "!coz", 
  "!tell /x"
 ], 
 "connections": {
  "local irc": {
   "actualaddress": "", 
   "admins": [], 
   "autotile": true, 
   "bots": [], 
   "bouncer-server": false, 
   "channels": [], 
   "ftp_dir": "", 
   "ftp_host": "", 
   "ftp_port": 21, 
   "ftp_pw": "", 
   "ftp_user": "", 
   "ignore": [], 
   "nick": "MyNewFrogBot", 
   "nickserv_password": "", 
   "owner": "Red_M", 
   "port": 6667, 
   "realname": "frog", 
   "reportchan": "#frog", 
   "rss-on": true, 
   "server": "aperture.esper.net", 
   "server_password": "", 
   "ssl": false, 
   "superadmins": ["Red_M"], 
   "twitterfeedchans": {}, 
   "user": "frog"
  }
 }, 
 "disabled_commands": [], 
 "disabled_plugins": [], 
 "log": "true", 
 "restartcmd": "bot.py"
}''') + '\n')

if not os.path.exists('./plugins/web/variables.vars'):
    open('./plugins/web/variables.vars', 'w').write(inspect.cleandoc(r''''''))


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
