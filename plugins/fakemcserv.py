from util import hook, perm, http
import re
import time
import Queue
import struct
import socket
import threading
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        getmcdata.append(str(self.client_address[0])+":"+str(self.client_address[1])+" wrote: "+str(response).replace("  ","").replace("\n","").replace("\\","\\\\"))
        #print str(self.client_address[0])+":"+str(self.client_address[1])+" wrote: "+response
        if data=="\x01":
            self.request.sendall("\x02")
        self.request.sendall("\x00\x07"+"\x20"*128+"\x00")
        self.request.sendall("\x0e"+mess+"\x20"*(64-len(mess)))
        playeramount.append(cur_thread.name)
        #self.request.sendall("\x00eDisconnected"+"\x20"*(64-len("Disconnected"))+"We have Moved..."+"\x20"*(64-len("We have Moved...")))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        time.sleep(2)
        data = []
        data.append(sock.recv(1024))
        testgetmcdata = "response: "+str(data).replace("  ","").replace("\\","\\\\")
    finally:
        sock.close()
        return testgetmcdata

@hook.command
def tcp(inp,bot=None,input=None):
    check = input.inp.split(" ")
    check2 = input.inp.replace(check[0]+" "+check[1],"")
    if perm.isowner(input):
        test = client(check[0],int(check[1]),check2)
        return test
        
@hook.command
def shut(inp,bot=None,input=None):
    bottest.shutdown()
    return "done."
    
@hook.command
def players(inp,input=None,bot=None):
    return bot.test["test"]
        
@hook.command
def mcmess(inp,bot=None,input=None):
    if perm.isowner(input):
        global mess
        mess = inp
        return "Done."
        
@hook.command
def fakemcserv(inp,bot=None,input=None):
    if perm.isowner(input):
        check = input.inp.split(" ")
        if len(check)==4:
            i = 0
            HOST, PORT = "", int(check[0])
            global bottest
            global getmcdata
            global playeramount
            global mess
            mess = "&6Player Moved too fast! (hacking?)"
            playeramount=["2"]
            getmcdata=[]
            bottest = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
            ip, portss = bottest.server_address
            global server_thread
            server_thread = threading.Thread(target=bottest.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            input.say("Server loop running in thread:"+server_thread.name)
            web = str(http.get("http://www.minecraft.net/heartbeat.jsp?port="+check[0]+"&max="+check[1]+"&name="+check[2]+"&public=True&version=7&salt=wo6kVAHjxoJcInKx&users="+check[3]))
            input.say(web)
            while True:
                web = str(http.get("http://www.minecraft.net/heartbeat.jsp?port="+check[0]+"&max="+check[1]+"&name="+check[2]+"&public=True&version=7&salt=wo6kVAHjxoJcInKx&users="+check[3]))
                if i==25:
                    i=0
                    input.say(web)
                plays = int(playeramount[len(playeramount)-1].replace("Thread-",""))
                bot.test["test"]=int(plays)-2
                i+=1
                time.sleep(45)
        else:
            return("error.")
    else:
        return("error. not high enough in my permissions to do this action.")