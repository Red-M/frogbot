import os
import sqlite3


def get_db_connection(conn, name=''):
    "returns an sqlite3 connection to a persistent database"

    if not name:
        name = '%s.%s.db' % (conn.nick, conn.name)
        
    filename = os.path.join(bot.persist_dir, name)
    return sqlite3.connect(filename, timeout=10)

bot.get_db_connection = get_db_connection

def get_db_connection_global(name=''):
    "returns an sqlite3 connection to a persistent database"

    if not name:
        name = 'global.db'

    filename = os.path.join(bot.persist_dir, name)
    return sqlite3.connect(filename, timeout=10)

bot.get_db_connection_global = get_db_connection_global
