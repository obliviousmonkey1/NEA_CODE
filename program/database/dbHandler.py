import sqlite3

"""
This handles for everything 
so have seperate functions for each database and stuff y
"""

class DBManager:
    def __init__(self, dbPath='') -> None:
        self.conn = sqlite3.connect(dbPath)
    

    # Population and people 
    def getPopulation(self, mapID):
        gPopulation = '''
        SELECT *
        FROM Person, Map, Population
        WHERE Map.ID = ? and Map.populationID = Population.id and Person.populationID = Population.id 
        '''
        c = self.conn.cursor()
        c.execute(gPopulation, (mapID,))
        return c.fetchall()   
    

    def updatePersonStatus(self, id: int, status: str) -> None:
        uPersonStatus = '''
        UPDATE Person
        SET status = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPersonStatus, (status, id))
        self.conn.commit()


    def updatePersonRtime(self, id: int, rTime: float) -> None:
        uPersonRtime = '''
        UPDATE Person
        SET rTime = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPersonRtime, (rTime, id))
        self.conn.commit()

    
    def updatePersonItime(self, id: int, iTime: float) -> None:
        uPersonItime = '''
        UPDATE Person
        SET iTime = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPersonItime, (iTime, id))
        self.conn.commit()


    def updatePersonXPos(self, id: int, pos: int) -> None:
        uPersonXPos = '''
        UPDATE Person
        SET xPos = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPersonXPos, (pos, id))
        self.conn.commit()


    def updatePersonYPos(self, id: int, pos: int) -> None:
        uPersonYPos = '''
        UPDATE Person
        SET yPos = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPersonYPos, (pos, id))
        self.conn.commit()


    # Map
    def getMaps(self):
        gMaps = '''
        SELECT *
        FROM Map
        '''
        c = self.conn.cursor()
        c.execute(gMaps)
        return c.fetchall()
    

    def getMapWidth(self, id: int) -> int:
        gMapWidth = '''
        SELECT width
        FROM Map
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gMapWidth, (id,))
        return c.fetchone()       


    def getMapHeight(self, id: int) -> int:
        gMapHeight = '''
        SELECT height
        FROM Map
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gMapHeight, (id,))
        return c.fetchone()    
    

    def getMapDay(self, id: int) -> int:
        gMapDay = '''
        SELECT day 
        FROM Map
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gMapDay, (id,))
        return c.fetchone()
        

    def updateMapDay(self, id: int, day: int) -> None:
        uMapDay = '''
        UPDATE Map
        SET day = ?
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uMapDay, (day, id))
        self.conn.commit()


    def close(self):
        self.conn.close()
        
db = DBManager()

db.close