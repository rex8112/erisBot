import sqlite3
import discord

db = sqlite3.connect('erisData.db')
cursor = db.cursor()

def initDB():	#initialize the database
	cursor.execute( """CREATE TABLE IF NOT EXISTS members( indx INTEGER PRIMARY KEY,
		name TEXT, id INTEGER UNIQUE, totalXP INTEGER DEFAULT 0, lvl INTEGER DEFAULT 1)""" )
	db.commit()
		
def addMem(mem: discord.Member): #add a member record
	name = mem.name
	id = mem.id
	cursor.execute( """INSERT INTO members(name, id)
										 VALUES(?, ?)""", (name, id))
	db.commit()
		
def updateXP(mem: discord.Member, amt): #Sets the XP of a member
	id = mem.id
	cursor.execute( """UPDATE members SET totalXP = ? WHERE id = ?""", (amt, id))
	db.commit()
	updateLVL(mem, amt)
	
def updateLVL(mem: discord.Member, xp): #Sets the lvl based on the XP given
	id = mem.id
	rxp = 500
	lvl = 1
	while xp >= rxp:
		rxp = rxp + 500 + (lvl * 100)
		lvl += 1
	cursor.execute("""UPDATE members SET lvl = ? WHERE id = ? """, (lvl, id))
	db.commit()

def getLVL(mem: discord.Member):
	id = mem.id
	cursor.execute( """SELECT lvl FROM members WHERE id = ?""", (id,))
	lvl = cursor.fetchone()
	if lvl:
		return lvl[0]
	else:
		return None
	
def getXP(mem: discord.Member):
	id = mem.id
	cursor.execute( """SELECT totalXP FROM members WHERE id = ?""", (id,))
	xp = cursor.fetchone()
	if xp:
		return xp[0]
	else:
		return None
		
def addXP(mem: discord.Member, amt):
	curxp = getXP(mem)
	newxp = curxp + amt
	updateXP(mem, newxp)
	return newxp
	
def remXP(mem: discord.Member, amt):
	curxp = getXP(mem)
	newxp = curxp - amt
	updateXP(mem, newxp)
	return newxp