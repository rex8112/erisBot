import datetime
import sqlite3
import discord
import logging


db = sqlite3.connect('erisData.db')
cursor = db.cursor()
logger = logging.getLogger('database')

class database:
    def initDB():   #initialize the database
        cursor.execute( """CREATE TABLE IF NOT EXISTS members( indx INTEGER PRIMARY KEY, name TEXT, id INTEGER UNIQUE, xp INTEGER DEFAULT 0, lvl INTEGER DEFAULT 0)""" )
        
        cursor.execute( """CREATE TABLE IF NOT EXISTS warnings( indx INTEGER PRIMARY KEY, name TEXT, id INTEGER, reason TEXT, warnerid INTEGER, date TEXT, state INTEGER DEFAULT 0)""")

        cursor.execute( """CREATE TABLE IF NOT EXISTS roles( indx INTEGER PRIMARY KEY, role TEXT UNIQUE, id INTEGER UNIQUE)""" )
        db.commit()
        
    def addMem(user: discord.Member): #add a member record
        name = user.name
        id = user.id
        cursor.execute( """INSERT INTO members(name, id)
                                             VALUES(?, ?)""", (name, id))
        db.commit()
        logger.info('{} Added to Database'.format(user))
            
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
            database.addMem(user)
            return database.getLVL(user)
        
    def getXP(user: discord.Member):
        id = user.id
        cursor.execute( """SELECT xp FROM members WHERE id = ?""", (id,))
        xp = cursor.fetchone()
        if xp:
            return xp[0]
        else:
            database.addMem(user)
            return database.getXP(user)
            
    def addXP(user: discord.Member, amt):
        curxp = database.getXP(user)
        newxp = curxp + amt
        database.updateXP(user, newxp)
        logger.debug('{}: {} Added to XP'.format(user, amt))
        return newxp
        
    def remXP(user: discord.Member, amt):
        curxp = database.getXP(user)
        newxp = curxp - amt
        database.updateXP(user, newxp)
        logger.debug('{}: {} Removed from XP'.format(user, amt))
        return newxp
        
    def getAllUsers():
        cursor.execute("""SELECT * FROM members""")
        return cursor.fetchall()
        
        
    def addLVL(user: discord.Member, amt):
        curlvl = database.getLVL(user)
        newlvl = curlvl + amt
        database.updateLVL(user, newlvl)
        logger.debug('{}: {} Added to Level'.format(user, amt))
        return newlvl
        
    def remLVL(user: discord.Member, amt):
        curlvl = database.getLVL(user)
        newlvl = curlvl - amt
        database.updateLVL(user, newlvl)
        logger.debug('{}: {} Removed from Level'.format(user, amt))
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
        
    def getAllWarn(page: int):
        p = (page - 1) * 10
        cursor.execute("""SELECT * FROM warnings ORDER BY indx DESC LIMIT 10 OFFSET ?""", (p,))
        warns = cursor.fetchall()
        return warns
        
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

    def listRole():
        cursor.execute( """SELECT * FROM roles ORDER BY indx LIMIT 10""" )
        roles = cursor.fetchall()
        return roles