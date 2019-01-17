import sqlite3
from passlib.hash import pbkdf2_sha256
import datetime

'''
user = "anarang"
user2 = "an"
user3 = "bn"
passw = "hassh"
'''

'''
tables
users: username, pass
coins: username, listCoins
threads: threadID, topic, post, user
user_threads (for each user): threadID, post
user_posts (for each user): threadID, postID, post
user_notifications (for each user): user, action, threadID, postID, read
t# (for each thread): postID, post, user, time, upvote, whoVote



'''


def reset(cursor):
    # this function resets the database
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
    v = "CREATE TABLE " + user + "_notifications (user TEXT, action TEXT, threadID INT, postID INT, read INT);"
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
def newThread(cursor,firstPost,user,topic):
    dt = str(datetime.datetime.now())
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
    cursor.execute(v,(1,firstPost,user,dt,0,""))
    if user != "Anonymous":
        v = "INSERT INTO " + user + "_threads VALUES(?,?);"
        cursor.execute(v,(currID,firstPost,))
        v = "INSERT INTO " + user + "_posts VALUES(?,?,?);"
        cursor.execute(v,(currID,1,firstPost))

def addToThread(cursor,post,threadID,user):
    dt = str(datetime.datetime.now())
    #print(dt)
    v = "SELECT postID FROM t" + str(threadID) + " ORDER BY postID DESC LIMIT 1;"
    t = cursor.execute(v).fetchone()[0] + 1
    if user!="Anonymous":
        v = "INSERT INTO " + user + "_posts VALUES(?,?,?);"
        cursor.execute(v,(threadID,t,post))
    v = "INSERT INTO t" + str(threadID) + " VALUES(?,?,?,?,?,?);"
    cursor.execute(v,(t,post,user,dt,0,""))
    v = "SELECT user FROM t" + str(threadID) + ";"

    #THIS ONLY RETURNS THE USER OF THE GENERAL THREAD, NOT PARTICULAR POSTS: IS THIS WHAT WE WANT?

    i = list(cursor.execute(v))[0]
    for j in i:
        v = "INSERT INTO " + j + "_notifications VALUES(?,?,?,?,?);"
        # user, post, threadID, postID, read
        cursor.execute(v,(user," responded to",threadID,t,0,))
    #cursor.execute(v,(user,'responded to',threadID,t,0,))
    # 0 means unread
    # 1 means read

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
     tee = "UPDATE t" + str(threadID) + " SET whoVote = ? WHERE postID = ?;"
     g = "SELECT upvote,whoVote,user FROM t" + str(threadID) + " WHERE postID = ?;"
     x = list(cursor.execute(g,(postID,)))
     temp = "INSERT INTO " + x[0][2] + "_notifications VALUES(?,?,?,?,?);"
    # (user TEXT, post TEXT, threadID INT, postID INT, read INT)
     x = list(cursor.execute(g,(postID,)))
    # print(x)
     if (len(x[0][1]) > 0):
         #print(x[0][1])
         t = x[0][1].split("!")
         #print(t)
         #print(user,t)
    #     print(user not in t)
         if user not in t:
             ha = x[0][0] + num
             print(t,user not in t)
             t.append(user)
             s = "!"
             print(t,user not in t)
             s = s.join(t)
            # print(s)
             cursor.execute(v,(ha,postID))
             cursor.execute(tee,(s,postID))
             if num is -1:
                 strToInsert = " downvoted"
             else:
                 strToInsert = " upvoted"
             cursor.execute(temp,(user,strToInsert,threadID,postID,0))
     elif x[0][2] is not user:
         ha = x[0][0] + num
         s = user + "!"
         #print(s,ha)
         cursor.execute(v,(ha,postID))
         cursor.execute(tee,(s,postID))

'''Notifs Functions'''

def getReadNotifs(cursor,user):
    v = "SELECT * FROM " + user + "_notifications WHERE read = ?;"
    return list(cursor.execute(v,(1,)))

def getUnreadNotifs(cursor,user):
    v = "SELECT * FROM " + user + "_notifications WHERE read = ?;"
    return list(cursor.execute(v,(0,)))

def readNotif(cursor,user,threadID,postID):
    # trigger refresh of page with notif gone to read
    v = "UPDATE " + user + "_notifications SET read = ? WHERE threadID = ? AND postID = ?;"
    cursor.execute(v,(1,threadID,postID,)) # turns this read

'''
db = sqlite3.connect('data/base.db')
c = db.cursor()
reset(c)
addUser(c,user,passw)
addUser(c,user2,passw)
addUser(c,user3,passw)
newThread(c,"bti",user,"be")
newThread(c,"baa",user2,"ba")
addToThread(c,"ha",1,user2)
votePost(c,2,1,1,user2)
votePost(c,2,1,1,user3)
votePost(c,2,1,1,user2)
votePost(c,2,1,1,user3)
votePost(c,2,1,1,user2)
print(viewThread(c,2))
db.commit()
db.close()
'''
