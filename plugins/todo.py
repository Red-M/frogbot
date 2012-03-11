from util import hook
import re

db_inited = False


def cleanSQL(sql):
    return re.sub(r'\s+', " ", sql).strip()


def db_init(db):
    global db_inited
    if db_inited:
        return

    exists = db.execute("""
      select exists (
        select * from sqlite_master where type = "table" and name = "todos"
      )
    """).fetchone()[0] == 1

    if not exists:
        db.execute(cleanSQL("""
           create virtual table todos using fts4(
                user,
                text,
                added,
                tokenize=porter
           )"""))

    db.commit()

    db_inited = True


def db_getall(db, nick, limit=-1):
    return db.execute("""
        select added, text
            from todos
            where user = ?
            order by added desc
            limit ?

        """, (nick, limit))


def db_get(db, nick, id):
    return db.execute("""
        select added, text from todos
        where user = ?
        order by added desc
        limit 1
        offset ?
    """, (nick, id)).fetchone()


def db_del(db, nick, limit='all'):
    row = db.execute("""
        delete from todos
        where rowid in (
          select rowid from todos
          where user = ?
          order by added desc
          limit ?
          offset ?)
     """, (nick,
          -1 if limit == 'all' else 1,
          0 if limit == 'all' else limit))
    db.commit()
    return row


def db_add(db, nick, text):
    db.execute("""
        insert into todos (user, text, added)
        values (?, ?, CURRENT_TIMESTAMP)
    """, (nick, text))
    db.commit()


def db_search(db, nick, query):
    return db.execute("""
        select added, text
        from todos
        where todos match ?
        and user = ?
        order by added desc
    """, (query, nick))


@hook.command
def todo(inp, nick='', chan='', db=None, notice=None, bot=None):
    "todo (add|del|list|search) [@user] args -- manipulates your todos"

    db_init(db)

    parts = inp.split()
    cmd = parts[0].lower()

    args = parts[1:]

    if len(args) and args[0].startswith("@"):
        nick = args[0][1:]
        args = args[1:]

    if cmd == 'add':
        if not len(args):
            return "no text"

        text = " ".join(args)

        db_add(db, nick, text)

        return "done."
    elif cmd == 'get':
        if len(args):
            try:
                index = int(args[0])
            except ValueError:
                return "Invalid number format."
        else:
            index = 0

        row = db_get(db, nick, index)

        if not row:
            return "none such entry."

        return "[%d]: %s: %s" % (index, row[0], row[1])
    elif cmd == 'del':
        if not len(args):
            return "error"

        if args[0] == 'all':
            index = 'all'
        else:
            try:
                index = int(args[0])
            except ValueError:
                return "invalid number"

        rows = db_del(db, nick, index)

        notice("Deleted %d entries" % rows.rowcount)
    elif cmd == 'list':
        limit = -1

        if len(args):
            try:
                limit = int(args[0])
                limit = max(-1, limit)
            except ValueError:
                return "invalid number"

        rows = db_getall(db, nick, limit)

        found = False

        for (index, row) in enumerate(rows):
            notice("[%d]: %s: %s" % (index, row[0], row[1]))
            found = True

        if not found:
            notice("%s has no entries." % nick)
    elif cmd == 'search':
        if not len(args):
            return "no search query given"

        query = " ".join(args)
        rows = db_search(db, nick, query)

        found = False

        for (index, row) in enumerate(rows):
            notice("[%d]: %s: %s" % (index, row[0], row[1]))
            found = True

        if not found:
            notice("%s has no matching entries for: %s" % (nick, query))

    else:
        return "unknown command: %s" % cmd
