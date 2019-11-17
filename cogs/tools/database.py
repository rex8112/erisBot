import datetime
import sqlite3
import discord
import logging


db = sqlite3.connect('erisData.db')
db2 = sqlite3.connect('corruption.db')
cursor = db.cursor()
cursor2 = db2.cursor()
logger = logging.getLogger('database')


def initDB():   #initialize the database
  cursor.execute( """CREATE TABLE IF NOT EXISTS members( indx INTEGER PRIMARY KEY, name TEXT, id INTEGER UNIQUE, xp INTEGER DEFAULT 0, lvl INTEGER DEFAULT 0)""" )
  
  cursor.execute( """CREATE TABLE IF NOT EXISTS warnings( indx INTEGER PRIMARY KEY, name TEXT, id INTEGER, reason TEXT, warnerid INTEGER, date TEXT, state INTEGER DEFAULT 0)""")

  cursor.execute( """CREATE TABLE IF NOT EXISTS roles( indx INTEGER PRIMARY KEY, role TEXT UNIQUE, id INTEGER UNIQUE)""" )
  
  cursor.execute( """CREATE TABLE IF NOT EXISTS roleplays( indx INTEGER PRIMARY KEY, name TEXT UNIQUE, category INTEGER, role INTEGER, private INTEGER, archived INTEGER DEFAULT 0)""" )

  cursor.execute( """CREATE TABLE IF NOT EXISTS adventurers( indx INTEGER PRIMARY KEY, id INTEGER UNIQUE, name TEXT, level INTEGER, str INTEGER, dex INTEGER, con INTEGER, int INTEGER, wis INTEGER, cha INTEGER, equipment TEXT, inventory TEXT)""" )

  cursor2.execute( """CREATE TABLE IF NOT EXISTS messages(cid INTEGER, mid INTEGER)""" )

  cursor2.execute( """CREATE TABLE IF NOT EXISTS roles(gid INTEGER, rid INTEGER, original TEXT)""")

  cursor2.execute( """CREATE TABLE IF NOT EXISTS categories(gid INTEGER, cid INTEGER, original TEXT)""" )

  cursor2.execute( """CREATE TABLE IF NOT EXISTS newcategories(gid INTEGER, cid INTEGER)""" )

  cursor2.execute( """CREATE TABLE IF NOT EXISTS channels(gid INTEGER, cid INTEGER)""" )
  db.commit()
  
def addMem(user: discord.Member): #add a member record
  name = user.name
  id = user.id
  cursor.execute( """INSERT INTO members(name, id)
                                          VALUES(?, ?)""", (name, id))
  db.commit()
  logger.info('{} Added to Database'.format(user))
  
def remMem(id): #remove a member record
  cursor.execute( """DELETE FROM members WHERE id = ?""", (id,) )
  db.commit()
  logger.warning('{}: Removed from Database'.format(id))
  
def updateXP(user: discord.Member, amt): #Sets the XP of a user
  id = user.id
  cursor.execute( """UPDATE members SET xp = ? WHERE id = ?""", (amt, id))
  db.commit()
  logger.debug('{}: XP set to {}'.format(user, amt))
    
def updateLVL(user: discord.Member, lvl): #Sets the lvl of a user
  id = user.id
  cursor.execute("""UPDATE members SET lvl = ? WHERE id = ? """, (lvl, id))
  db.commit()
  logger.debug('{}: Level set to {}'.format(user, lvl))

def getLVL(user: discord.Member):
  id = user.id
  cursor.execute( """SELECT lvl FROM members WHERE id = ?""", (id,))
  lvl = cursor.fetchone()
  if lvl:
      return lvl[0]
  else:
      addMem(user)
      return getLVL(user)
  
def getXP(user: discord.Member):
  id = user.id
  cursor.execute( """SELECT xp FROM members WHERE id = ?""", (id,))
  xp = cursor.fetchone()
  if xp:
      return xp[0]
  else:
      addMem(user)
      return getXP(user)
  
def addXP(user: discord.Member, amt):
  curxp = getXP(user)
  newxp = curxp + amt
  updateXP(user, newxp)
  logger.debug('{}: {} Added to XP'.format(user, amt))
  return newxp
  
def remXP(user: discord.Member, amt):
  curxp = getXP(user)
  newxp = curxp - amt
  updateXP(user, newxp)
  logger.debug('{}: {} Removed from XP'.format(user, amt))
  return newxp
  
def getAllUsers():
  cursor.execute("""SELECT * FROM members""")
  return cursor.fetchall()
  
def addLVL(user: discord.Member, amt):
  curlvl = getLVL(user)
  newlvl = curlvl + amt
  updateLVL(user, newlvl)
  logger.debug('{}: {} Added to Level'.format(user, amt))
  return newlvl
  
def remLVL(user: discord.Member, amt):
  curlvl = getLVL(user)
  newlvl = curlvl - amt
  updateLVL(user, newlvl)
  logger.debug('{}: {} Removed from Level'.format(user, amt))
  return newlvl
  
def addWarn(user: discord.Member, reason, warner: discord.Member):
  name = user.name
  id = user.id
  wid = warner.id
  today = datetime.date.today()
  cursor.execute("""INSERT INTO warnings(name, id, reason, warnerid, date) VALUES(?, ?, ?, ?, ?)""", (name, id, reason, wid, today))
  db.commit()
  
def remWarn(indx):
  cursor.execute("""DELETE FROM warnings WHERE indx = ?""", (indx,))
  db.commit()
  
def getWarn(user: discord.Member):
  id = user.id
  cursor.execute("""SELECT * FROM warnings WHERE id = ?""", (id,))
  warns = cursor.fetchall()
  return warns
  
def getAllWarn(page: int):
  p = (page - 1) * 10
  cursor.execute("""SELECT * FROM warnings ORDER BY indx DESC LIMIT 10 OFFSET ?""", (p,))
  warns = cursor.fetchall()
  return warns
  
def pardonWarn(indx: int):
  cursor.execute("""UPDATE warnings SET state = 1 WHERE indx = ?""", (indx,))
  db.commit()
  
def leaderboard():
  cursor.execute("""SELECT id, lvl, xp FROM members ORDER BY lvl DESC, xp DESC LIMIT 10""")
  users = cursor.fetchall()
  return users

def addRole(role):
  name = role.name
  id = role.id
  try:
      cursor.execute( """INSERT INTO roles(role, id) VALUES(?, ?)""",(name, id) )
  except sqlite3.IntegrityError:
      return 'Role already exists, try removing and adding again'
  db.commit()

def remRole(role):
  id = role.id
  cursor.execute( """DELETE FROM roles WHERE id = ?""", (id,) )
  db.commit()
  
def getRole(role):
  id = role.id
  cursor.execute( """SELECT role, id FROM roles WHERE id = ?""", (id,) )
  target = cursor.fetchone()
  return target
  
def listRole():
  cursor.execute( """SELECT * FROM roles ORDER BY indx LIMIT 10""" )
  roles = cursor.fetchall()
  return roles
  
def addRP(name, cat: int, role: int, private: bool):
  if private:
      private = 1
  else:
      private = 0
      
  cursor.execute( """INSERT INTO roleplays(name, category, role, private) VALUES(?, ?, ?, ?)""", (name, cat, role, private) )
  db.commit()
  
def delRP(name):
  cursor.execute( """DELETE FROM roleplays WHERE name = ?""", (name,) )
  db.commit()

def getAdventurer(id):
  cursor.execute( """SELECT * FROM adventurers WHERE id = ?""", (id,) )
  return cursor.fetchone()

def addCMessage(cid: int, mid: int):
  cursor2.execute( """INSERT INTO messages(cid, mid) VALUES(?, ?)""", (cid, mid) )
  db2.commit()

def getCMessages():
  cursor2.execute( """SELECT cid, mid FROM messages""" )
  return cursor2.fetchall()

def remCMessage(mid: int):
  cursor2.execute( """DELETE FROM messages WHERE mid = ?""", (mid,) )
  db2.commit()

def addNewCategory(gid: int, cid: int):
  cursor2.execute( """INSERT INTO newcategories(gid, cid) VALUES(?, ?)""", (gid, cid) )
  db2.commit()

def getNewCategory():
  cursor2.execute( """SELECT gid, cid FROM newcategories""" )
  return cursor2.fetchall()

def remNewCategory(cid: int):
  cursor2.execute( """DELETE FROM newcategories WHERE cid = ?""", (cid,) )
  db2.commit()

def addChannel(gid: int, cid: int):
  cursor2.execute( """INSERT INTO channels(gid, cid) VALUES(?, ?)""", (gid, cid) )
  db2.commit()

def getChannel():
  cursor2.execute( """SELECT gid, cid FROM channels""" )
  return cursor2.fetchall()

def remChannel(cid: int):
  cursor2.execute( """DELETE FROM channels WHERE cid = ?""", (cid,) )
  db2.commit()

def addCategory(gid: int, cid: int, original: str):
  cursor2.execute( """INSERT INTO categories(gid, cid, original) VALUES(?, ?, ?)""", (gid, cid, original) )
  db2.commit()

def getCategory():
  cursor2.execute( """SELECT gid, cid, original FROM categories""" )
  return cursor2.fetchall()

def remCategory(cid: int):
  cursor2.execute( """DELETE FROM categories WHERE cid = ?""", (cid,) )
  db2.commit()