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
    exist = cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = ?);", (foo_char_html(user),))
    return exist.fetchone()[0] == 1

def check_pass(cursor, user, passE): # checks if password is correct
    toCheck = cursor.execute("SELECT pass from users WHERE username = ?;", (foo_char_html(user),))

    try:
        return pbkdf2_sha256.verify(passE.encode("ascii", "replace"), toCheck.fetchone()[0])
    except:
        return False

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
    cursor.execute("INSERT INTO threads VALUES(?,?,?,?);",(str(currID),topic, firstPost, user)) # adds the thread to overall
    #order did not match that of creation--Home Affairs

    v = "CREATE TABLE t" + str(currID) + " (postID INT PRIMARY KEY,post TEXT,user TEXT,time TEXT,upvote INT,whoVote TEXT);" # makes the thread table
    cursor.execute(v)
    v = "INSERT INTO t" + str(currID) + " VALUES(?,?,?,?,?,?);"
    cursor.execute(v,(1,firstPost,user,datetime,0,""))
    if user != "Anonymous":
        v = "INSERT INTO " + user + "_threads VALUES(?,?);"
        cursor.execute(v,(currID,firstPost,))
        v = "INSERT INTO " + user + "_posts VALUES(?,?,?);"
        cursor.execute(v,(currID,1,firstPost))

def addToThread(cursor,post,threadID,user,datetime):
    v = "SELECT postID FROM t" + str(threadID) + " ORDER BY postID DESC LIMIT 1;"
    t = cursor.execute(v).fetchone()[0] + 1
    if user!="Anonymous":
        v = "INSERT INTO " + user + "_posts VALUES(?,?,?);"
        cursor.execute(v,(threadID,t,post))
    v = "INSERT INTO t" + str(threadID) + " VALUES(?,?,?,?,?,?);"
    cursor.execute(v,(t,post,user,datetime,0,""))

def viewThreads(cursor):
    val = list(cursor.execute("SELECT * FROM threads;"))
    return val

def viewThread(cursor,threadID):
    v = "SELECT user,post,time,postID,upvote,whoVote FROM t" + str(threadID) + ";" # not the people who upvote
    val = list(cursor.execute(v))
    return val

def viewTopic(cursor,topi):
    l = list(cursor.execute("SELECT threadID,user,post FROM threads WHERE topic = ?;",(topi,)))
    return l

def userThreads(cursor,user):
    v = "SELECT post,threadID FROM " + user + "_threads;"
    l = list(cursor.execute(v))
    return l

def userPosts(cursor,user):
    v = "SELECT * FROM " + user + "_posts;"
    l = list(cursor.execute(v))
    return l

def votePost(cursor,threadID,postID,num,user):
     v = "UPDATE t" + str(threadID) + " SET upvote = ? WHERE postID = ?;"
     t = "UPDATE t" + str(threadID) + " SET whoVote = ? WHERE postID = ?;"
     g = "SELECT upvote,whoVote FROM t" + str(threadID) + " WHERE postID = ?;"
     x = list(cursor.execute(g,(postID,)))
    # print(x)
     if (len(x[0][1]) > 0):
         t = x[0][1].split("!")
         if user not in t:
             ha = x[0][0] + num
             t.append(user)
             s = "!"
             s = s.join(ha)
             cursor.execute(v,(str(ha),postID,s))
     else:
         ha = x[0][0] + num
         s = user + "!"
         print(s,ha)
         cursor.execute(v,(ha,postID))
         cursor.execute(t,(s,postID))

db = sqlite3.connect('base.db')
c = db.cursor()
reset(c)

addUser(c,user,passw)
reset(c)
'''
newThread(c,"bti",user,"333","be")
newThread(c,"baa",user,"323","ba")
addToThread(c,"ha",1,user,"3333")
print(viewThreads(c))
print(viewThread(c,2))
votePost(c,2,1,-1,user)
v = viewThread(c,2)
print(v)
'''
db.commit()
db.close()
