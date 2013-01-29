import cherrypy
import os
import sys
import time
import json
import socket
from mako.template import Template
from mako.lookup import TemplateLookup
import ast
import dircache

current_dir = os.path.dirname(os.path.abspath(__file__))
if os.name == 'posix':
    lookup = TemplateLookup(directories=[current_dir+'/templates'])
if os.name == 'nt':
    lookup = TemplateLookup(directories=[current_dir+'\\templates'])
    
    
import sqlite3
if os.name == 'posix':
    persdir = current_dir.replace("/plugins/util","/persist")
if os.name == 'nt':
    persdir = current_dir.replace("\\plugins"+"\\"+"util","\\"+"persist")

def get_db_connection(ourdir,name):
    "returns an sqlite3 connection to a persistent database"
    filename = os.path.join(ourdir, name)
    return sqlite3.connect(filename, timeout=10)

def factoidrefresh(persdir):
    list = dircache.listdir(persdir)
    list2=[]
    x=-1
    factoiddb = {}
    testone = {}
    table = {}
    for file in list:
        if str(file).endswith(".db"):
            x=x+1
            list2.append(str(file))
    if "global.db" in list2:
        list2.remove("global.db")
    for file in list2:
        factoiddb[file] = get_db_connection(persdir,file)
        testone[file] = factoiddb[file].execute("SELECT * FROM memory where chan=(?)",("Red_M",)).fetchall()
        table[file] = []
        for data in testone[file]:
            (chan,word,wordata,wordnick) = data
            table[file].append('<td align="left" style="width:10%">?'+word.replace('>', '&gt;').replace('<', '&lt;')+"</td>\n    "+'<td align="left" style="width:80%"><div style="word-wrap: break-word;">'+wordata.replace('>', '&gt;').replace('<', '&lt;')+"</div></td>\n    "+'<td align="left" style="width:10%">'+wordnick+"</td>")
        factoiddb[file].close()
    return table
        
def serve_template(tmpl, **kwargs):
    """ loads a template and renders it """
    tmpl = lookup.get_template(tmpl)
    return tmpl.render(**kwargs)
    
def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        data = {}
        data = ast.literal_eval(sock.recv(1024*16).replace("\\%s" % ("\\"), \
                                                                        "\\"))
    finally:
        sock.close()
        return data

        
class CommandsPage:
    @cherrypy.expose
    def index(self):
        input = client("127.0.0.1",4329,"requesting bot variable data " \
        "refreshment. please respond.")
        return serve_template("commands.mako", title="Commmands", \
        nick=input['nick'], commands=input['cmds'], \
        cmdlen=str(int(input['cmdlen']+1)))
        
        
class AboutPage:
    @cherrypy.expose
    def index(self):
        input = client("127.0.0.1",4329,"requesting bot variable data " \
        "refreshment. please respond.")
        return serve_template("about.mako", title="About", \
        nick=input['nick'], channels=input['channels'], \
        pyver=input['pythonver'], host=input['host'], \
        os=input['os'], bit=input['bit'], uptime=input['uptime'], \
        mem=input['mem'], players=input['players'])
        
        
class FactoidsPage:
    @cherrypy.expose
    def index(self):
        input = client("127.0.0.1",4329,"requesting bot variable data " \
        "refreshment. please respond.")
        word = factoidrefresh(persdir)
        return serve_template("factoids.mako", title="Factoids", nick=input['nick'], word=word)
        
        
class HelpPage:
    @cherrypy.expose
    def index(self):
        input = client("127.0.0.1",4329,"requesting bot variable data " \
        "refreshment. please respond.")
        return serve_template("help.mako", title="Help", \
        nick=input['nick'], channels=input['channels'], \
        pyver=input['pythonver'], host=input['host'], os=input['os'], \
        bit=input['bit'], uptime=input['uptime'], mem=input['mem'], \
        players=input['players'])
        
        
class StatusPage:
    @cherrypy.expose
    def index(self):
        input = client("127.0.0.1",4329,"requesting bot variable data " \
        "refreshment. please respond.")
        return serve_template("status.mako", title="Status", \
        nick=input['nick'], channels=input['channels'], \
        pyver=input['pythonver'], host=input['host'], os=input['os'], \
        bit=input['bit'], uptime=input['uptime'], mem=input['mem'], \
        players=input['players'])
        
        

class WebInterface:
    """ main web interface class """
    help = HelpPage()
    commands = CommandsPage()
    factoids = FactoidsPage()
    about = AboutPage()
    status = StatusPage()
    scp = SCPPage()
    @cherrypy.expose
    def index(self):
        input = client("127.0.0.1",4329,"requesting bot variable data " \
        "refreshment. please respond.")
        return serve_template("index.mako", title="FrogBot", \
        nick=input['nick'], channels=input['channels'], \
        pyver=input['pythonver'], host=input['host'], os=input['os'], \
        bit=input['bit'], uptime=input['uptime'], mem=input['mem'], \
        players=input['players'])
        

def web_init(inp,inputs=None,bot=None):
    print "Initalising web server..."
    global input
    input = {}
    global_conf = {
        'global': { 'engine.autoreload.on': False,
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8080,
        'log.error_file': 'site.log',
        'log.screen': False
    }}
    application_conf = {
        '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir,
        'static'),
        }
    }
    cherrypy.config.update(global_conf)
    web_interface = WebInterface()
    print("Web server started")
    cherrypy.quickstart(web_interface, '/', config = application_conf)