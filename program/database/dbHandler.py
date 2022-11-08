import sqlite3
import os 
"""
This handles for everything 
so have seperate functions for each database and stuff y
"""

class DBManager:
    def __init__(self, dbPath=os.path.expanduser('~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db')) -> None:
        self.conn = sqlite3.connect(dbPath)
    

    # Population and people 
    def createPopulation(self, id: int, susceptible: int, infected: int, removed: int) -> None:
        cPopulation = '''
        INSERT INTO Population VALUES
        (?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cPopulation, (id,susceptible,infected,removed))
        self.conn.commit()


    def getPopulationSusceptible(self, id: int) -> None:
        gPopulationSusceptible = '''
        SELECT Population.susceptible
        FROM Population
        WHERE Population.id = ?
        '''
        c = self.conn.cursor()
        c.execute(gPopulationSusceptible, (id,))
        return c.fetchone()   


    def getPopulationInfected(self, id: int) -> None:
        gPopulationInfected = '''
        SELECT Population.infected
        FROM Population
        WHERE Population.id = ?
        '''
        c = self.conn.cursor()
        c.execute(gPopulationInfected, (id,))
        return c.fetchone()  


    def getPopulationRemoved(self, id: int) -> None:
        gPopulationRemoved = '''
        SELECT Population.removed
        FROM Population
        WHERE Population.id = ?
        '''
        c = self.conn.cursor()
        c.execute(gPopulationRemoved, (id,))
        return c.fetchone()  


    def updatePopulationSusceptible(self, id: int, susceptible: int) -> None:
        uPopulationSusceptible = '''
        UPDATE Population
        SET susceptible = ?
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPopulationSusceptible, (susceptible, id))
        self.conn.commit()


    def updatePopulationInfected(self, id: int, infected: int) -> None:
        uPopulationInfected = '''
        UPDATE Population
        SET infected = ?
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPopulationInfected, (infected, id))
        self.conn.commit()


    def updatePopulationRemoved(self, id: int, removed: int) -> None:
        uPopulationRemoved = '''
        UPDATE Population
        SET removed = ?
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPopulationRemoved, (removed, id))
        self.conn.commit()


    def createPerson(self, id: int, status: str, rTime: float, iTime: float, ibTime: float, travellingTime: float,travelling:int,asymptomatoc: int, paritalImmunity:float,destination:int,bloodType:str,age:int,health:float, xPos: int, yPos: int, diseaseID: int, populationID: int) -> None:
        cPerson = '''
        INSERT INTO Person VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cPerson, (id,status,rTime,iTime,ibTime,travellingTime,travelling,asymptomatoc,paritalImmunity,destination,bloodType,age,health,xPos,yPos,diseaseID,populationID))
        self.conn.commit()


    def getPopulation(self, mapID):
        gPopulation = '''
        SELECT Person.id, Person.status, Person.rTime, Person.iTime, Person.ibTime, Person.travellingTime, Person.travelling, Person.asymptomatic, Person.paritalImmunity, Person.destination, Person.bloodType, Person.age, Person.health, Person.xPos, Person.yPos, Person.diseaseID
        FROM Person, Map, Population
        WHERE Map.ID = ? and Map.populationID = Population.id and Person.populationID = Population.id 
        '''
        c = self.conn.cursor()
        c.execute(gPopulation, (mapID,))
        return c.fetchall()   
    

    def updatePersonID(self, id: int, newID: int) -> None:
        uPersonID = '''
        UPDATE Person
        SET id = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPersonID, (newID, id))
        self.conn.commit()


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
    def createMap(self, id: int, name: str, width: int, height: int, day: int,govermentActionReliabilty:float,identifyAndIsolateTriggerInfectionCount:int,infectionTimeBeforeQuarantine:float,socialDistanceTriggerInfectionCount:int, populationID: int) -> None:
        cMap = '''
        INSERT INTO Map VALUES
        (?,?,?,?,?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cMap, (id, name, width, height, day,govermentActionReliabilty,identifyAndIsolateTriggerInfectionCount,infectionTimeBeforeQuarantine,socialDistanceTriggerInfectionCount, populationID))
        self.conn.commit()


    def getMaps(self):
        gMaps = '''
        SELECT *
        FROM Map
        '''
        c = self.conn.cursor()
        c.execute(gMaps)
        return c.fetchall()
    

    def getMapIDs(self):
        gMapIDs = '''
        SELECT id 
        FROM Map
        '''
        c = self.conn.cursor()
        c.execute(gMapIDs)
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
    def createDisease(self, id: str, name: str, transmissionTime: float, contagion: float, transmissionRadius: int, infectedTime: float, incubationTime: float,ageMostSusceptible:int,canKill:int,pAsymptomaticOnInfection:float,danger:float) -> None:
        cDisease = '''
        INSERT INTO Disease VALUES
        (?,?,?,?,?,?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cDisease, (id, name, transmissionTime, contagion, transmissionRadius, infectedTime, incubationTime,ageMostSusceptible,canKill,pAsymptomaticOnInfection,danger))
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


    def getDiseasetPasymptomatic(self, id: str) -> float:
        gPasymptomaticOnInfection = '''
        SELECT pAsymptomaticOnInfection
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gPasymptomaticOnInfection, (id,))
        return c.fetchone()


    # Blood Type
    def createBloodType(self, id: int, bloodType: str) -> None:
        cBloodType = '''
        INSERT INTO BloodType VALUES
        (?,?)
        '''
        c = self.conn.cursor()
        c.execute(cBloodType, (id, bloodType))
        self.conn.commit()
    

    def createDiseaseBloodTypeLink(self, diseaseID: str, bloodTypeID: int) -> None:
        cCreateDiseaseBloodTypeLinkTable = '''
        INSERT INTO DiseaseBloodTypeLink VALUES
        (?,?)
        '''
        c = self.conn.cursor()
        c.execute(cCreateDiseaseBloodTypeLinkTable, (diseaseID, bloodTypeID))
        self.conn.commit()


    def close(self):
        self.conn.close()
        