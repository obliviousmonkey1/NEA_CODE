import sqlite3

"""
This handles for everything 
so have seperate functions for each database and stuff y
"""

class DBManager:
    def __init__(self, dbPath='') -> None:
        self.conn = sqlite3.connect(dbPath)
    

    # Population and people 
    def createPopulation(self, id: int) -> None:
        cPopulation = '''
        INSERT INTO Population VALUES
        (?)
        '''
        c = self.conn.cursor()
        c.execute(cPopulation, (id,))
        self.conn.commit()


    def createPerson(self, id: int, status: str, rTime: float, iTime: float, ibTime: float, xPos: int, yPos: int, travelling: bool, travellingTime: float, originalHome: int, diseaseID: int, populationID: int) -> None:
        cPerson = '''
        INSERT INTO Person VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cPerson, (id,status,rTime,iTime,ibTime,xPos,yPos,travelling,travellingTime,originalHome,diseaseID,populationID))
        self.conn.commit()


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


    def updatePersonIBtime(self, id: int, ibTime: float) -> None:
        uPersonIBtime = '''
        UPDATE Person
        SET ibTime = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPersonIBtime, (ibTime, id))
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


    def updateDiseaseID(self, id: int, diseaseID: int) -> None:
        uPersonDiseaseID = '''
        UPDATE Person
        SET diseaseID = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPersonDiseaseID, (diseaseID, id))
        self.conn.commit()


    # Map
    def createMap(self, id: int, name: str, width: int, height: int, day: int, populationID: int) -> None:
        cMap = '''
        INSERT INTO Map VALUES
        (?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cMap, (id, name, width, height, day, populationID))
        self.conn.commit()


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


    # Disease
    def createDisease(self, id: str, name: str, transmissionTime: float, contagion: float, transmissionRadius: int, infectedTime: float, incubationTime: float) -> None:
        cDisease = '''
        INSERT INTO Disease VALUES
        (?,?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cDisease, (id, name, transmissionTime, contagion, transmissionRadius, infectedTime, incubationTime))
        self.conn.commit()


    def getDiseaseName(self, id: str) -> str:
        gDiseaseName = '''
        SELECT name
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseName, (id,))
        return c.fetchone()    


    def getDiseaseTransmissionTime(self, id: str) -> float:
        gDiseaseTransmissionTime = '''
        SELECT transmissionTime
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseTransmissionTime, (id,))
        return c.fetchone()    


    def getDiseaseContagion(self, id: str) -> float:
        gDiseaseContagion = '''
        SELECT contagion
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseContagion, (id,))
        return c.fetchone()    


    def getDiseaseTransmissionRadius(self, id: str) -> int:
        gDiseaseTransmissionRadius = '''
        SELECT transmissionRadius
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseTransmissionRadius, (id,))
        return c.fetchone()    


    def getDiseaseInfectedTime(self, id: str) -> float:
        gInfectedTime = '''
        SELECT infectedTime
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gInfectedTime, (id,))
        return c.fetchone()
    

    def getDiseaseIncubationTime(self, id: str) -> float:
        gIncubationTime = '''
        SELECT incubationTime
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gIncubationTime, (id,))
        return c.fetchone()


    # Statistics
    def createStatistics(self, id: str, day: int, map: int, susceptible: int, infected: int, removed: int) -> None:
        cStatistics = '''
        INSERT INTO Statistics VALUES
        (?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cStatistics, (id, day, map, susceptible, infected, removed))
        self.conn.commit()


    def getAllSusceptible(self, day: int) -> int:
        gAllSusceptible = '''
        SELECT susceptible
        FROM Statistics
        WHERE day = ? 
        '''
        c = self.conn.cursor()
        c.execute(gAllSusceptible, (day,))
        return c.fetchall()


    def getAllInfected(self, day: int) -> int:
        gAllInfected = '''
        SELECT infected
        FROM Statistics
        WHERE day = ?
        '''
        c = self.conn.cursor()
        c.execute(gAllInfected, (day,))
        return c.fetchall()


    def getAllRemoved(self, day: int) -> int:
        gAllRemoved = '''
        SELECT removed
        FROM Statistics
        WHERE day = ?
        '''
        c = self.conn.cursor()
        c.execute(gAllRemoved, (day,))
        return c.fetchall()


    def getAllSusceptibleFromMap(self, day: int, mapID: int) -> int:
        gAllSusceptibleFromMap= '''
        SELECT susceptible
        FROM Statistics
        WHERE day = ? and map = ? 
        '''
        c = self.conn.cursor()
        c.execute(gAllSusceptibleFromMap, (day, mapID))
        return c.fetchone()


    def getAllInfectedFromMap(self, day: int, mapID: int) -> int:
        gAllInfectedFromMap= '''
        SELECT infected
        FROM Statistics
        WHERE day = ? and map = ? 
        '''
        c = self.conn.cursor()
        c.execute(gAllInfectedFromMap, (day, mapID))
        return c.fetchone()


    def getAllRemovedFromMap(self, day: int, mapID: int) -> int:
        gAllRemovedFromMap= '''
        SELECT removed
        FROM Statistics
        WHERE day = ? and map = ? 
        '''
        c = self.conn.cursor()
        c.execute(gAllRemovedFromMap, (day, mapID))
        return c.fetchone()


    def close(self):
        self.conn.close()
        