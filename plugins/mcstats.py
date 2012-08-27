# code from Luke edited by Red_M on espernet or Red-M on github.com
from util import http,hook
import json

@hook.command(autohelp=False)
def mcstatus(inp, say=None):
    request = http.get("http://status.mojang.com/check")

    # make the shitty json less shitty, cbf parsing it normally
    data = json.loads(request.replace("}", "").replace("{", "").replace("]", "}").replace("[", "{"))

    outt = ""
    out = ""
    i=0
    # use a loop so we don't have to update it if they add more servers
    for server, status in data.items():
        i+=1
        if status == "green":
            if i==len(data):
                outt += ("%s online." % server.replace("login.minecraft.net","login is").replace("account.mojang.com","accounts are").replace("auth.mojang.com","authentication is").replace("session.minecraft.net","sessions are"))
            else:
                outt += ("%s online, " % server.replace("login.minecraft.net","login is").replace("account.mojang.com","accounts are").replace("auth.mojang.com","authentication is").replace("session.minecraft.net","sessions are"))
        else:
            if i==len(data):
                outt += ("%s offline." % server.replace("login.minecraft.net","login is").replace("account.mojang.com","accounts are").replace("auth.mojang.com","authentication is").replace("session.minecraft.net","sessions are"))
            else:
                outt += ("%s offline, " % server.replace("login.minecraft.net","login is").replace("account.mojang.com","accounts are").replace("auth.mojang.com","authentication is").replace("session.minecraft.net","sessions are"))
    out=outt.replace(", minecraft.net ",", The minecraft website is ")
    return out