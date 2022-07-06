import sqlite3

db = sqlite3.connect("links.db")
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS links (link TEXT, short TEXT)")
db.commit()
cur.close()
db.close()


def checkIfShortExists(short):
    db = sqlite3.connect("links.db")
    cur = db.cursor()
    cur.execute("SELECT short FROM links WHERE short = ?", (short,))
    result = cur.fetchone()
    cur.close()
    db.close()
    return result

def addLink(link, short):
    db = sqlite3.connect("links.db")
    cur = db.cursor()
    cur.execute("INSERT INTO links (link, short) VALUES (?, ?)", (link, short))
    cur.close()
    db.commit()
    db.close()

def getLink(short):
    db = sqlite3.connect("links.db")
    cur = db.cursor()
    cur.execute("SELECT link, short FROM links WHERE short = ?", (short,))
    result = cur.fetchone()
    cur.close()
    db.close()
    return result[0]
