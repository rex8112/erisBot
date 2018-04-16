import sqlite3
import discord
db = sqlite3.connect('eris')

cursor = db.cursor()

def initDB():
	cursor.execute( """CREATE TABLE IF NOT EXISTS members( index INTEGER PRIMARY KEY,
		name TEXT, id INTEGER UNIQUE, totalXP INTEGER)""" )
		
def addMem(mem: discord.Member):
	name = mem.name
	id = mem.id
	cursor.execute( """INSERT INTO members(name, id)
										 VALUES(?, ?)""", (name, id))
		
def updateXP(mem: discord.Member, amt):
	id = mem.id
	cursor.execute( """UPDATE members SET totalXP = ? WHERE id = ?""", (amt, id))
	
def getXP(mem: discord.Member):
	id = mem.id
	cursor.execute( """SELECT totalXP FROM members WHERE id = ?""", (id))
	xp = cursor.fetchone()
	return xp[0]