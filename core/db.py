import os
import sqlite3


def get_db_connection(conn, name=''):
    "returns an sqlite3 connection to a persistent database"

    if not name:
        name = '%s.%s.db' % (conn.nick, conn.conf["server"])

    filename = os.path.join(bot.persist_dir, name)
    return sqlite3.connect(filename, timeout=10)

bot.get_db_connection = get_db_connection

def get_db_connection_auth(name=''):
    "returns an sqlite3 connection to a persistent database"

    if not name:
        name = 'auth.db'

    filename = os.path.join(bot.persist_dir, name)
    return sqlite3.connect(filename, timeout=10)

bot.get_db_connection_auth = get_db_connection_auth

def get_db_connection_twitter(name=''):
    "returns an sqlite3 connection to a persistent database"

    if not name:
        name = 'twitter.db'

    filename = os.path.join(bot.persist_dir, name)
    return sqlite3.connect(filename, timeout=10)

bot.get_db_connection_twitter = get_db_connection_twitter
