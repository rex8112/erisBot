import datetime
import sqlite3
import discord


db = sqlite3.connect('erisData.db')
cursor = db.cursor()

class database:
	def initDB():	#initialize the database
		cursor.execute( """CREATE TABLE IF NOT EXISTS members( indx INTEGER PRIMARY KEY,
			name TEXT, id INTEGER UNIQUE, xp INTEGER DEFAULT 0, lvl INTEGER DEFAULT 0)""" )
		
		cursor.execute( """CREATE TABLE IF NOT EXISTS warnings( indx INTEGER PRIMARY KEY, name TEXT, id INTEGER, reason TEXT, warnerid INTEGER, date TEXT, state INTEGER DEFAULT 0)""")
		db.commit()
			
	def addMem(user: discord.Member): #add a member record
		name = user.name
		id = user.id
		cursor.execute( """INSERT INTO members(name, id)
											 VALUES(?, ?)""", (name, id))
		db.commit()
			
	def updateXP(user: discord.Member, amt): #Sets the XP of a user
		id = user.id
		cursor.execute( """UPDATE members SET xp = ? WHERE id = ?""", (amt, id))
		db.commit()
		
	def updateLVL(user: discord.Member, lvl): #Sets the lvl of a user
		id = user.id
		cursor.execute("""UPDATE members SET lvl = ? WHERE id = ? """, (lvl, id))
		db.commit()

	def getLVL(user: discord.Member):
		id = user.id
		cursor.execute( """SELECT lvl FROM members WHERE id = ?""", (id,))
		lvl = cursor.fetchone()
		if lvl:
			return lvl[0]
		else:
			print('DB: User \'{}\' Not Found, Adding Record'.format(user))
			database.addMem(user)
			return database.getLVL(user)
		
	def getXP(user: discord.Member):
		id = user.id
		cursor.execute( """SELECT xp FROM members WHERE id = ?""", (id,))
		xp = cursor.fetchone()
		if xp:
			return xp[0]
		else:
			print('DB: User \'{}\' Not Found, Adding Record'.format(user))
			database.addMem(user)
			return database.getXP(user)
			
	def addXP(user: discord.Member, amt):
		curxp = database.getXP(user)
		newxp = curxp + amt
		database.updateXP(user, newxp)
		return newxp
		
	def remXP(user: discord.Member, amt):
		curxp = database.getXP(user)
		newxp = curxp - amt
		database.updateXP(user, newxp)
		return newxp
		
	def addLVL(user: discord.Member, amt):
		curlvl = database.getLVL(user)
		newlvl = curlvl + amt
		database.updateLVL(user, newlvl)
		return newlvl
		
	def remLVL(user: discord.Member, amt):
		curlvl = database.getLVL(user)
		newlvl = curlvl - amt
		database.updateLVL(user, newlvl)
		return newlvl
		
	def addWarn(user: discord.Member, reason, warner: discord.Member):
		name = user.name
		id = user.id
		wid = warner.id
		today = datetime.date.today()
		cursor.execute("""INSERT INTO warnings(name, id, reason, warnerid, date) VALUES(?, ?, ?, ?, ?)""", (name, id, reason, wid, today))
		db.commit()
		
	def getWarn(user: discord.Member):
		id = user.id
		cursor.execute("""SELECT * FROM warnings WHERE id = ?""", (id,))
		warns = cursor.fetchall()
		return warns