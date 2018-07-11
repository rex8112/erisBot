import sqlite3
import discord

db = sqlite3.connect('erisData.db')
cursor = db.cursor()

class database:
	def initDB():	#initialize the database
		cursor.execute( """CREATE TABLE IF NOT EXISTS members( indx INTEGER PRIMARY KEY,
			name TEXT, id INTEGER UNIQUE, totalXP INTEGER DEFAULT 0, lvl INTEGER DEFAULT 1)""" )
		
		cursor.execute( """CREATE TABLE IF NOT EXISTS warnings( indx INTEGER PRIMARY KEY, name TEXT, id INTEGER, reason TEXT, state INTEGER DEFAULT 0)""")
		db.commit()
			
	def addMem(user: discord.Member): #add a member record
		name = user.name
		id = user.id
		cursor.execute( """INSERT INTO members(name, id)
											 VALUES(?, ?)""", (name, id))
		db.commit()
			
	def updateXP(user: discord.Member, amt): #Sets the XP of a member
		id = user.id
		cursor.execute( """UPDATE members SET totalXP = ? WHERE id = ?""", (amt, id))
		db.commit()
		database.updateLVL(user, amt)
		
	def updateLVL(user: discord.Member, xp): #Sets the lvl based on the XP given
		id = user.id
		rxp = 300
		lvl = 1
		while xp >= rxp:
			rxp = rxp + 300 + (lvl * 100)
			lvl += 1
		cursor.execute("""UPDATE members SET lvl = ? WHERE id = ? """, (lvl, id))
		db.commit()

	def getLVL(user: discord.Member):
		id = user.id
		cursor.execute( """SELECT lvl FROM members WHERE id = ?""", (id,))
		lvl = cursor.fetchone()
		if lvl:
			return lvl[0]
		else:
			return 1
		
	def getXP(user: discord.Member):
		id = user.id
		cursor.execute( """SELECT totalXP FROM members WHERE id = ?""", (id,))
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
		
	def addWarn(user: discord.Member, reason):
		name = user.name
		id = user.id
		cursor.execute("""INSERT INTO warnings(name, id, reason) VALUES(?, ?, ?)""", (name, id, reason))
		db.commit()
		
	def getWarn(user: discord.Member):
		id = user.id
		cursor.execute("""SELECT * FROM warnings WHERE id = ?""", (id,))
		warns = cursor.fetchall()
		return warns