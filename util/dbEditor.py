import sqlite3
from passlib.hash import pbkdf2_sha256

user = "anarang"
passw = "hassh"

def reset(cursor):
    tables = list(cursor.execute("select name from sqlite_master where type is 'table'"))
    cursor.executescript(';'.join(["drop table if exists %s" %i for i in tables])) # got inspo for this from a stackOverflow post
    cursor.execute("CREATE TABLE users (username TEXT PRIMARY KEY, pass TEXT);")
    cursor.execute("CREATE TABLE coins (username TEXT PRIMARY KEY, listCoins TEXT);")
    cursor.execute("CREATE TABLE threads (threadID INT PRIMARY KEY, topic TEXT, post TEXT, user TEXT);")

'''User Functions'''
def addUser(cursor,user,passE): # adds user info to tables
    cursor.execute("INSERT INTO users VALUES(?, ?);", (foo_char_html(user), pbkdf2_sha256.hash(passE.encode("ascii", "replace"))))
    cursor.execute("INSERT INTO coins VALUES(?, ?);", (foo_char_html(user),""))
    v = "CREATE TABLE " + user + "_threads (threadID INT PRIMARY KEY, post TEXT);"
    cursor.execute(v)
    v = "CREATE TABLE " + user + "_posts (threadID INT, postID INT, post TEXT);"
    cursor.execute(v)

def userExists(cursor,user): # checks if user exists
    exist = cursor.execute("SELECT EXISTS((SELECT 1 FROM users WHERE username = ?);", (foo_char_html(user),))
    return exist.fetchone()[0] == 1

def check_pass(cursor, user, passE): # checks if password is correct
    toCheck = cursor.execute("SELECT pass from users WHERE username = ?;", (foo_char_html(user),))
    return pbkdf2_sha256.verify(passE.encode("ascii", "replace"), toCheck.fetchone()[0])

def foo_char_html(str): # parses through username
    return str.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

'''Coin Functions'''
def getCoins(cursor,user): # get list of coins user likes
    t = cursor.execute("SELECT listCoins from coins WHERE username = ?;", (foo_char_html(user),)).fetchone()[0]
    val = t.split("!")
    return val

def likeCoin(cursor,user,coin): # add coin user likes
    t = cursor.execute("SELECT listCoins from coins WHERE username = ?;", (foo_char_html(user),)).fetchone()[0]
    t = t + coin + "!"
    cursor.execute("UPDATE coins SET listCoins = ? WHERE username = ?;",(t,foo_char_html(user),))

'''Thread Functions'''
def newThread(cursor,firstPost,user,datetime,topic):
    t = cursor.execute("SELECT threadID FROM threads ORDER BY threadID DESC LIMIT 1;").fetchone()
    if t is None:
        currID = 1
    else:
        currID = t[0] + 1
    cursor.execute("INSERT INTO threads VALUES(?,?,?,?);",(str(currID),firstPost,user,topic)) # adds the thread to overall
    v = "CREATE TABLE t" + str(currID) + " (postID INT PRIMARY KEY,post TEXT,user TEXT,time TEXT);" # makes the thread table
    cursor.execute(v)
    v = "INSERT INTO t" + str(currID) + " VALUES(?,?,?,?);"
    cursor.execute(v,(1,firstPost,user,datetime,))
    v = "INSERT INTO " + user + "_threads VALUES(?,?);"
    cursor.execute(v,(currID,firstPost,))
    v = "INSERT INTO " + user + "_posts VALUES(?,?,?);"
    cursor.execute(v,(currID,1,firstPost))

def addToThread(cursor,post,threadID,user,datetime):
    v = "SELECT postID FROM t" + str(threadID) + " ORDER BY postID DESC LIMIT 1;"
    t = cursor.execute(v).fetchone()[0] + 1
    v = "INSERT INTO " + user + "_posts VALUES(?,?,?);"
    cursor.execute(v,(threadID,t,post))
    v = "INSERT INTO t" + str(threadID) + " VALUES(?,?,?,?);"
    cursor.execute(v,(t,post,user,datetime))

def viewThreads(cursor):
    val = list(cursor.execute("SELECT * FROM threads;"))
    return val

def viewThread(cursor,threadID):
    v = "SELECT * FROM t" + str(threadID) + ";"
    val = list(cursor.execute(v))
    return val

db = sqlite3.connect('base.db')
c = db.cursor()
reset(c)
'''
addUser(c,user,passw)
newThread(c,"he",user,"333","bti")
newThread(c,"heee",user,"323","baa")
addToThread(c,"ha",1,user,"3333")
t = viewThread(c,1)
print(t)
t = viewThreads(c)
print(t)
'''
db.commit()
db.close()
