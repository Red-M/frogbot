from util import hook, perm, http
import SimpleHTTPServer
import BaseHTTPServer
import SocketServer

def run_while_true(server_class,handler_class,bot):
    server_address = ('', 8000)
    bot.htmlserv = server_class(server_address, handler_class)
    while bot.html==1:
        bot.htmlserv.handle_request()

def run(inp,bot,input):
    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    bot.html = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT
    bot.html.serve_forever()
    return bot.html

@hook.command
def webshut(inp,bot=None,input=None):
    if perm.isowner(input):
        if bot.html==1:
            bot.html=0
            return "done. webserver is off."
        else:
            return "webserver is already off."
    
@hook.command
def webserv(inp,bot=None,input=None):
    if perm.isowner(input):
        if bot.html==0:
            bot.html=1
            baseserver = BaseHTTPServer.HTTPServer
            serverhandler = SimpleHTTPServer.SimpleHTTPRequestHandler
            run_while_true(baseserver,serverhandler,bot)
            return "done. webserver is now on."
        else:
            return("my webserver is already on.")