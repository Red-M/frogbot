#!/usr/bin/env python
import cherrypy
import os.path
import time
import json
import socket
from mako.template import Template
from mako.lookup import TemplateLookup
import ast

current_dir = os.path.dirname(os.path.abspath(__file__))
lookup = TemplateLookup(directories=[current_dir+'/templates'])
        
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
        return serve_template("factoids.mako", title="Factoids", \
        nick=input['nick'], channels=input['channels'], \
        pyver=input['pythonver'], host=input['host'], os=input['os'], \
        bit=input['bit'], uptime=input['uptime'], mem=input['mem'], \
        players=input['players'])
        
        
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
        
        
class SCPPage:
    @cherrypy.expose
    def index(self):
        return serve_template("scp.mako", title="SCP ideas")
        

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
        

def web_init():
    print "Initalising web server..."
    global input
    input = {}
    global_conf = {
        'global': { 'engine.autoreload.on': True,
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
    cherrypy.tree.mount(web_interface, '/', config = application_conf)
    cherrypy.server.start()
    cherrypy.engine.start()
web_init()
