import sqlite3
import discord

db = sqlite3.connect('eris.db')
cursor = db.cursor()

def initDB():	
	cursor.execute( """CREATE TABLE IF NOT EXISTS members( indx INTEGER PRIMARY KEY,
		name TEXT, id INTEGER UNIQUE, totalXP INTEGER)""" )
	db.commit()
		
def addMem(mem: discord.Member):
	name = mem.name
	id = mem.id
	cursor.execute( """INSERT INTO members(name, id)
										 VALUES(?, ?)""", (name, id))
	db.commit()
		
def updateXP(mem: discord.Member, amt):
	id = mem.id
	cursor.execute( """UPDATE members SET totalXP = ? WHERE id = ?""", (amt, id))
	db.commit()
	
def getXP(mem: discord.Member):
	id = mem.id
	cursor.execute( """SELECT totalXP FROM members WHERE id = ?""", (id,))
	xp = cursor.fetchone()
	if xp:
		return xp[0]
	else:
		return None