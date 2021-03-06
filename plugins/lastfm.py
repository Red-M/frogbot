'''
The Last.fm API key is retrieved from the bot config file.
'''

from util import hook, http


api_url = "http://ws.audioscrobbler.com/2.0/?format=json"


@hook.command
def lastfm(inp, nick='', say=None, bot=None):
    api_key = bot.config.get("api_keys", {}).get("lastfm", None)
    if not api_key:
        return None

    if inp:
        user = inp
    else:
        user = nick

    response = http.get_json(api_url, method="user.getrecenttracks",
                             api_key=api_key, user=user, limit=1)

    if 'error' in response:
        if inp:  # specified a user name
            return "error: %s" % response["message"]
        else:
            return "your nick is not a Last.fm account. try '.lastfm username'."

    if not "track" in response["recenttracks"] or len(response["recenttracks"]["track"]) == 0:
        return "no recent tracks for user \x02%s\x0F found" % user

    tracks = response["recenttracks"]["track"]

    if type(tracks) == list:
        # if the user is listening to something, the tracks entry is a list
        # the first item is the current track
        track = tracks[0]
        status = 'current track'
    elif type(tracks) == dict:
        # otherwise, they aren't listening to anything right now, and
        # the tracks entry is a dict representing the most recent track
        track = tracks
        status = 'last track'
    else:
        return "error parsing track listing"

    title = track["name"]
    album = track["album"]["#text"]
    artist = track["artist"]["#text"]

    ret = "\x02%s\x0F's %s - \x02%s\x0f" % (user, status, title)
    if artist:
        ret += " by \x02%s\x0f" % artist
    if album:
        ret += " on \x02%s\x0f" % album

    say(ret)

