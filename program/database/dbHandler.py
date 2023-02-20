import sqlite3
import os 


class DBManager:
    def __init__(self, dbPath=os.path.expanduser('~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db')) -> None:
        self.conn = sqlite3.connect(dbPath)
    

    # Population and people 
    # adds in new data to a new column population table
    def createPopulation(self, id: int, susceptible: int, infected: int, removed: int) -> None:
        cPopulation = '''
        INSERT INTO Population VALUES
        (?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cPopulation, (id,susceptible,infected,removed))
        self.conn.commit()


    # gets the value of the current suscpetible row for a certain id
    def getPopulationSusceptible(self, id: int) -> None:
        gPopulationSusceptible = '''
        SELECT Population.susceptible
        FROM Population
        WHERE Population.id = ?
        '''
        c = self.conn.cursor()
        c.execute(gPopulationSusceptible, (id,))
        return c.fetchone()   


    # gets the value of the current infected row for a certain id
    def getPopulationInfected(self, id: int) -> None:
        gPopulationInfected = '''
        SELECT Population.infected
        FROM Population
        WHERE Population.id = ?
        '''
        c = self.conn.cursor()
        c.execute(gPopulationInfected, (id,))
        return c.fetchone()  


    # gets the value of the current removed row for a certain id
    def getPopulationRemoved(self, id: int) -> None:
        gPopulationRemoved = '''
        SELECT Population.removed
        FROM Population
        WHERE Population.id = ?
        '''
        c = self.conn.cursor()
        c.execute(gPopulationRemoved, (id,))
        return c.fetchone()  


    # updates the value of the susceptible row for a certain id 
    def updatePopulationSusceptible(self, id: int, susceptible: int) -> None:
        uPopulationSusceptible = '''
        UPDATE Population
        SET susceptible = ?
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPopulationSusceptible, (susceptible, id))
        self.conn.commit()


    # updates the value of the infected row for a certain id 
    def updatePopulationInfected(self, id: int, infected: int) -> None:
        uPopulationInfected = '''
        UPDATE Population
        SET infected = ?
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPopulationInfected, (infected, id))
        self.conn.commit()


    # updates the value of the removed row for a certain id 
    def updatePopulationRemoved(self, id: int, removed: int) -> None:
        uPopulationRemoved = '''
        UPDATE Population
        SET removed = ?
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPopulationRemoved, (removed, id))
        self.conn.commit()


    # adds in new data to a new column pawn table
    def createPawn(self, id: int, status: str, rTime: float, iTime: float, ibTime: float, travellingTime: float, travelling:int,
                    asymptomatoc: int, paritalImmunity:float,destination:int,bloodType:str,age:int,health:float, xPos: int, yPos: int,
                     diseaseID: int, populationID: int) -> None:
        cPawn = '''
        INSERT INTO Pawn VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cPawn, (id,status,rTime,iTime,ibTime,travellingTime,0.0,travelling,asymptomatoc,paritalImmunity,populationID,destination,bloodType,age,health,xPos,yPos,0.0,0,0,0,0,0,diseaseID,populationID))
        self.conn.commit()


    # gets the values of all the population 
    def getPopulation(self, mapID):
        gPopulation = '''
        SELECT Pawn.id, Pawn.status, Pawn.rTime, Pawn.iTime, Pawn.ibTime, Pawn.tTime, Pawn.ntTime, Pawn.travelling, Pawn.asymptomatic, Pawn.paritalImmunity, Pawn.sDestination, Pawn.destination, Pawn.bloodType, Pawn.age, Pawn.health, Pawn.xPos, Pawn.yPos, Pawn.qTime, Pawn.qInfected, Pawn.qTravelling, Pawn.arrivalCheck, Pawn.isInfectious, Pawn.isIncubating, Pawn.diseaseID
        FROM Pawn, Map, Population
        WHERE Map.ID = ? and Map.populationID = Population.id and Pawn.populationID = Population.id 
        '''
        c = self.conn.cursor()
        c.execute(gPopulation, (mapID,))
        return c.fetchall()   
    

    # updates the value of the populationID row for a certain id 
    def updatePawnPopulationID(self, id: int, newID: int) -> None:
        uPawnPopulationID = '''
        UPDATE Pawn
        SET populationID = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnPopulationID, (newID, id))
        self.conn.commit()


    # updates the value of the status row for a certain id 
    def updatePawnStatus(self, id: int, status: str) -> None:
        uPawnStatus = '''
        UPDATE Pawn
        SET status = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnStatus, (status, id))
        self.conn.commit()


    # updates the value of the destination row for a certain id 
    def updatePawnDestination(self, id: int, destination: str) -> None:
        uPawnDestination = '''
        UPDATE Pawn
        SET destination = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnDestination, (destination, id))
        self.conn.commit()


    # updates the value of the travelling row for a certain id 
    def updatePawnTravelling(self, id: int, travelling: int) -> None:
        uPawnTravelling = '''
        UPDATE Pawn
        SET travelling = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnTravelling, (travelling, id))
        self.conn.commit()


    # updates the value of the radius time row for a certain id 
    def updatePawnRtime(self, id: int, rTime: float) -> None:
        uPawnRtime = '''
        UPDATE Pawn
        SET rTime = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnRtime, (rTime, id))
        self.conn.commit()
    

    # updates the value of the travel time row for a certain id 
    def updatePawnTtime(self, id: int, tTime: float) -> None:
        uPawnTtime = '''
        UPDATE Pawn
        SET tTime = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnTtime, (tTime, id))
        self.conn.commit()

    
    # updates the value of the infection time row for a certain id 
    def updatePawnItime(self, id: int, iTime: float) -> None:
        uPawnItime = '''
        UPDATE Pawn
        SET iTime = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnItime, (iTime, id))
        self.conn.commit()


    # updates the value of the quarantine time row for a certain id 
    def updatePawnQtime(self, id: int, qTime: float) -> None:
        uPawnQtime = '''
        UPDATE Pawn
        SET qTime = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnQtime, (qTime, id))
        self.conn.commit()


    # updates the value of the incubation time row for a certain id 
    def updatePawnIBtime(self, id: int, ibTime: float) -> None:
        uPawnIBtime = '''
        UPDATE Pawn
        SET ibTime = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnIBtime, (ibTime, id))
        self.conn.commit()


    # updates the value of the time since last travelled row for a certain id 
    def updatePawnNTtime(self, id: int, ntTime: float) -> None:
        uPawnNTtime = '''
        UPDATE Pawn
        SET ntTime = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnNTtime, (ntTime, id))
        self.conn.commit()


    # updates the value of the x position row for a certain id 
    def updatePawnXPos(self, id: int, pos: int) -> None:
        uPawnXPos = '''
        UPDATE Pawn
        SET xPos = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnXPos, (pos, id))
        self.conn.commit()


    # updates the value of the y position row for a certain id 
    def updatePawnYPos(self, id: int, pos: int) -> None:
        uPawnYPos = '''
        UPDATE Pawn
        SET yPos = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnYPos, (pos, id))
        self.conn.commit()


    # updates the value of the boolean quarantined infected row for a certain id 
    def updateQinfected(self, id: int, qInfected: int) -> None:
        uQinfected = '''
        UPDATE Pawn
        SET qInfected = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uQinfected, (qInfected, id))
        self.conn.commit()


    # updates the value of the boolean quarantined travelling row for a certain id 
    def updateQtravelling(self, id: int, qTravelling: int) -> None:
        uQtravelling = '''
        UPDATE Pawn
        SET qTravelling = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uQtravelling, (qTravelling, id))
        self.conn.commit()


    # updates the value of arrival check row for a certain id 
    def updateArrivalCheck(self, id: int, arrivalCheck: int) -> None:
        uArrivalCheck = '''
        UPDATE Pawn
        SET arrivalCheck = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uArrivalCheck, (arrivalCheck, id))
        self.conn.commit()


    # updates the value of the boolean is infectious row for a certain id 
    def updateIsInfectious(self, id: int, isInfectious: int) -> None:
        uPawnIsInfectious = '''
        UPDATE Pawn
        SET isInfectious = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnIsInfectious, (isInfectious, id))
        self.conn.commit()


    # updates the value of the boolean is incubating row for a certain id 
    def updateIsIncubating(self, id: int, isIncubating: int) -> None:
        uPawnIsIncubating = '''
        UPDATE Pawn
        SET isIncubating = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnIsIncubating, (isIncubating, id))
        self.conn.commit()


    # updates the value of the disease identifier row for a certain id 
    def updateDiseaseID(self, id: int, diseaseID: int) -> None:
        uPawnDiseaseID = '''
        UPDATE Pawn
        SET diseaseID = ? 
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uPawnDiseaseID, (diseaseID, id))
        self.conn.commit()


    # Map
    # adds in new data to a new column map table
    def createMap(self, id: int, name: str, width: int, height: int, day: int,govermentActionReliabilty:float,
                 identifyAndIsolateTriggerInfectionCount:int,infectionTimeBeforeQuarantine:float,travelQuarintineTime:float,socialDistanceTriggerInfectionCount:int,
                 travelProhibitedTriggerInfectionCount:int,travelTime:float, travelProhibited:int, populationID: int) -> None:
        cMap = '''
        INSERT INTO Map VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cMap, (id, name, width, height, day,govermentActionReliabilty,identifyAndIsolateTriggerInfectionCount,infectionTimeBeforeQuarantine,travelQuarintineTime,socialDistanceTriggerInfectionCount,travelProhibitedTriggerInfectionCount,travelTime,travelProhibited, populationID))
        self.conn.commit()


    # gets the values of all the maps
    def getMaps(self):
        gMaps = '''
        SELECT *
        FROM Map
        '''
        c = self.conn.cursor()
        c.execute(gMaps)
        return c.fetchall()
    

    # gets the values of all map ids that aren't equal to the one passed as an argument
    def getMapIDs(self,id):
        gMapIDs = '''
        SELECT Map.id 
        FROM Map
        WHERE Map.id != ?
        '''
        c = self.conn.cursor()
        c.execute(gMapIDs,(id,))
        return c.fetchall()


    # gets the values of all map ids 
    def getAllMapIDs(self):
        gAllMapIDs = '''
        SELECT Map.id 
        FROM Map
        '''
        c = self.conn.cursor()
        c.execute(gAllMapIDs)
        return c.fetchall()


    # gets the value of the current map width row for a certain id
    def getMapWidth(self, id: int) -> int:
        gMapWidth = '''
        SELECT width
        FROM Map
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gMapWidth, (id,))
        return c.fetchone()       


    # gets the value of the current map height row for a certain id
    def getMapHeight(self, id: int) -> int:
        gMapHeight = '''
        SELECT height
        FROM Map
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gMapHeight, (id,))
        return c.fetchone()    
    

    # gets the value of the current map day row for a certain id
    def getMapDay(self, id: int) -> int:
        gMapDay = '''
        SELECT day 
        FROM Map
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gMapDay, (id,))
        return c.fetchone()
    

    # gets the value of the current travel time row for a certain id
    def getMapTravelTime(self, id: int) -> float:
        gMapTravelTime = '''
        SELECT travelTime 
        FROM Map
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gMapTravelTime, (id,))
        return c.fetchone()


    # gets the value of the current boolen travel prohibited row for a certain id
    def getMapCannnotTravelTo(self, id: int) -> float:
        gMapCannnotTravelTo = '''
        SELECT travelProhibited 
        FROM Map
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gMapCannnotTravelTo, (id,))
        return c.fetchone()
        

    # updates the value of the day row for a certain id 
    def updateMapDay(self, id: int, day: int) -> None:
        uMapDay = '''
        UPDATE Map
        SET day = ?
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uMapDay, (day, id))
        self.conn.commit()
    
    
    # updates the value of the boolean travel prohibited row for a certain id 
    def updateMapCannotTravelTo(self, id: int, value: int) -> None:
        uMapCanTravelTo = '''
        UPDATE Map
        SET travelProhibited = ?
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(uMapCanTravelTo, (value, id))
        self.conn.commit()


    # Disease
    # adds in new data to a new column disease table
    def createDisease(self, id: str, name: str, transmissionTime: float, contagion: float, transmissionRadius: int,
                     infectedTime: float, incubationTime: float,ageMostSusceptible:int,virulence:float,pAsymptomaticOnInfection:float,
                     mutationChance:float) -> None:
        cDisease = '''
        INSERT INTO Disease VALUES
        (?,?,?,?,?,?,?,?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cDisease, (id, name, transmissionTime, contagion, transmissionRadius, infectedTime, incubationTime,ageMostSusceptible,virulence,pAsymptomaticOnInfection,mutationChance))
        self.conn.commit()


    # gets the value of the current name row for a certain id
    def getDiseaseName(self, id: str) -> str:
        gDiseaseName = '''
        SELECT name
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseName, (id,))
        return c.fetchone()    


    # gets the value of the current transmission time row for a certain id
    def getDiseaseTransmissionTime(self, id: str) -> float:
        gDiseaseTransmissionTime = '''
        SELECT transmissionTime
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseTransmissionTime, (id,))
        return c.fetchone()    


    # gets the value of the current contagion row for a certain id
    def getDiseaseContagion(self, id: str) -> float:
        gDiseaseContagion = '''
        SELECT contagion
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseContagion, (id,))
        return c.fetchone()    


    # gets the value of the current transmission radius row for a certain id
    def getDiseaseTransmissionRadius(self, id: str) -> int:
        gDiseaseTransmissionRadius = '''
        SELECT transmissionRadius
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseTransmissionRadius, (id,))
        return c.fetchone()    


    # gets the value of the current infected time row for a certain id
    def getDiseaseInfectedTime(self, id: str) -> float:
        gInfectedTime = '''
        SELECT infectedTime
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gInfectedTime, (id,))
        return c.fetchone()
    

    # gets the value of the current incubation time row for a certain id
    def getDiseaseIncubationTime(self, id: str) -> float:
        gIncubationTime = '''
        SELECT incubationTime
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gIncubationTime, (id,))
        return c.fetchone()


    # gets the value of the current probabilty of asymptomatic on infection row for a certain id
    def getDiseasetPasymptomatic(self, id: str) -> float:
        gPasymptomaticOnInfection = '''
        SELECT pAsymptomaticOnInfection
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gPasymptomaticOnInfection, (id,))
        return c.fetchone()


    # gets the value of the current mutation chance row for a certain id
    def getDiseaseMutationChance(self, id: str) -> float:
        gDiseaseMutationChance = '''
        SELECT mutationChance
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseMutationChance, (id,))
        return c.fetchone()


    # gets the value of the current disease mutation row for a certain id
    def getDiseaseMutation(self, id: str) -> float:
        gDiseaseMutationChance = '''
        SELECT *
        FROM Disease
        WHERE id = ?
        '''
        c = self.conn.cursor()
        c.execute(gDiseaseMutationChance, (id,))
        return c.fetchall()


    # Blood Type
    # adds in new data to a new column blood type table
    def createBloodType(self, id: int, bloodType: str) -> None:
        cBloodType = '''
        INSERT INTO BloodType VALUES
        (?,?)
        '''
        c = self.conn.cursor()
        c.execute(cBloodType, (id, bloodType))
        self.conn.commit()
    

    # adds in new data to a new column disease blood type relational table
    def createDiseaseBloodTypeLink(self, diseaseID: str, bloodTypeID: int) -> None:
        cCreateDiseaseBloodTypeLinkTable = '''
        INSERT INTO DiseaseBloodTypeLink VALUES
        (?,?)
        '''
        c = self.conn.cursor()
        c.execute(cCreateDiseaseBloodTypeLinkTable, (diseaseID, bloodTypeID))
        self.conn.commit()


    # General 
    # adds in new data to a new column general table
    def createGeneral(self, generalMutationChance: float, numberOfMaps: int, timeRequiredBetweenTravels: float) -> None:
        cGeneral = '''
        INSERT INTO General VALUES
        (?,?,?,?)
        '''
        c = self.conn.cursor()
        c.execute(cGeneral, (0,generalMutationChance,numberOfMaps,timeRequiredBetweenTravels))
        self.conn.commit()


    # gets the value of the current general mutation chance row for a certain id
    def getGeneralMutationChance(self, id: int):
        gGeneralMutationChance = '''
        SELECT General.generalMutationChance
        FROM General
        WHERE General.id = ? 
        '''
        c = self.conn.cursor()
        c.execute(gGeneralMutationChance, (id,))
        return c.fetchone() 


    # gets the value of the current number of maps row for a certain id
    def getNumberOfMaps(self, id: int):
        gNumberOfMaps = '''
        SELECT General.numberOfMaps
        FROM General
        WHERE General.id = ? 
        '''
        c = self.conn.cursor()
        c.execute(gNumberOfMaps, (id,))
        return c.fetchone()   
    

    # gets the value of the current time required between travels row for a certain id
    def getTimeRequiredBetweenTravels(self, id: int):
        gTimeRequiredBetweenTravels = '''
        SELECT General.timeRequiredBetweenTravels
        FROM General
        WHERE General.id = ? 
        '''
        c = self.conn.cursor()
        c.execute(gTimeRequiredBetweenTravels, (id,))
        return c.fetchone()   


    # Stats 
    # gets the value of the current population travelling row for a certain id
    def getPopulationTravelling(self, id: int):
        gPopulationTravelling = '''
        SELECT *
        FROM Pawn
        WHERE Pawn.populationID = ? AND Pawn.travelling = 1
        '''
        c = self.conn.cursor()
        c.execute(gPopulationTravelling, (id,))
        return c.fetchall()  
    

    # gets the values of the current population travelling row for a certain id 
    def getPopulationTravelling(self, id: int):
        gPopulationTravelling = '''
        SELECT Pawn.destination
        FROM Pawn
        WHERE Pawn.populationID = ? AND Pawn.travelling = 1
        '''
        c = self.conn.cursor()
        c.execute(gPopulationTravelling, (id,))
        return c.fetchall()  


    # gets the values of the current disease ids in a map row for a certain id and if status is I
    def getAllDiseaseIDsInAmap(self, id: int):
        gPopulationTravelling = '''
        SELECT Pawn.diseaseID
        FROM Pawn
        WHERE Pawn.populationID = ? AND Pawn.status = ?
        '''
        c = self.conn.cursor()
        c.execute(gPopulationTravelling, (id,'I'))
        return c.fetchall()  


    # gets the value of all the disease rows for a certain id
    def getAllDiseaseInfoFromID(self, id: int):
        gAllDiseaseInfoFromID = '''
        SELECT *
        FROM Disease
        WHERE Disease.id = ? 
        '''
        c = self.conn.cursor()
        c.execute(gAllDiseaseInfoFromID, (id,))
        return c.fetchone()  
    
    
    # gets the values of the current quarintined infected row for a certain id
    def getPopulationQuarintineInfected(self, id: int):
        gPopulationQuarintineInfected = '''
        SELECT Pawn.qInfected
        FROM Pawn
        WHERE Pawn.populationID = ?  AND Pawn.qInfected = ?
        '''
        c = self.conn.cursor()
        c.execute(gPopulationQuarintineInfected, (id,1))
        return c.fetchall()  


    # gets the values of the current population travelling row for a certain id
    def getPopulationQuarintineTravelling(self, id: int):
        gPopulationQuarintineTravelling = '''
        SELECT Pawn.qTravelling
        FROM Pawn
        WHERE Pawn.populationID = ? AND Pawn.qTravelling = ?
        '''
        c = self.conn.cursor()
        c.execute(gPopulationQuarintineTravelling, (id,1))
        return c.fetchall()  


    # gets the values of the current infected incubating row for a certain id and if a Pawn isnt travelling
    def getInfectedIncubating(self, id: int):
        gInfectedIncubating = '''
        SELECT Pawn.isIncubating
        FROM Pawn
        WHERE Pawn.populationID = ? AND Pawn.isIncubating = ? AND Pawn.travelling = ?
        '''
        c = self.conn.cursor()
        c.execute(gInfectedIncubating, (id,1,0))
        return c.fetchall()  


    # gets the values of the current infectious row for a certain id and if the Pawn isn't travelling
    def getInfectedInfectious(self, id: int):
        gInfectedInfectious = '''
        SELECT Pawn.isInfectious
        FROM Pawn
        WHERE Pawn.populationID = ? AND Pawn.isInfectious = ? AND Pawn.travelling = ?
        '''
        c = self.conn.cursor()
        c.execute(gInfectedInfectious, (id,1,0))
        return c.fetchall()  


    def close(self):
        self.conn.close()
        