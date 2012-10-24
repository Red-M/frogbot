#!/usr/bin/env python
#import server
#server.web_init()
import os
import dircache
import sqlite3
curdir = "/plugins/web/start.py"
pers = "/persist"
persdir = os.path.abspath(__file__).replace(curdir,pers)

def get_db_connection(ourdir,name):
    "returns an sqlite3 connection to a persistent database"
    filename = os.path.join(ourdir, name)
    return sqlite3.connect(filename, timeout=10)

list = dircache.listdir(persdir)
list2=[]
x=-1
factoiddb = {}
testone = {}
tableword = {}
tablewordata = {}
tablewordnick = {}

for file in list:
    if str(file).endswith(".db"):
        x=x+1
        list2.append(str(file))
list2.remove("global.db")
for file in list2:
    factoiddb[file] = get_db_connection(persdir,file)
    testone[file] = factoiddb[file].execute("SELECT * FROM memory where chan=(?)",("Red_M",)).fetchall()
    tableword[file] = []
    tablewordata[file] = []
    tablewordnick[file] = []
    for data in testone[file]:
        (chan,word,wordata,wordnick) = data
        tableword[file].append(word)
        tablewordata[file].append(wordata)
        tablewordnick[file].append(wordnick)
        #print(data)
    
#print(testone[list2[1]])