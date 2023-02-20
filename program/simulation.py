FILE_PATH_DBH = '~/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_DB = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'
FILE_PATH_LOG = '~/Documents/NEA/NEA_CODE/program/inhouse tools'
FILE_PATH_SETTINGS = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json'


import sys
import os
sys.path.append(os.path.expanduser(FILE_PATH_LOG))
sys.path.append(os.path.expanduser(FILE_PATH_DBH))

import dbHandler as dbH
import logger  
import random
import timeit
import json
import csv 


'''
S - Susceptible
I - Infected
R - Removed
people randomly move about map and if they are within the area of contagion of an infected pawn for 
x amount of time they become infected SIR model 
'''


# Constants 
MAX_MOVE_AMOUNT = 2
MOVE_PROBABILITY = 0.5
TRAVEL_RATE = 0.999
P_INFECTION_PER_DAY = 1 
MUTATIONS = []
       

class Simulation:
    def __init__(self, map) -> None:
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))
        self.__disease = Disease(self.__dbQueryHandler)
        self.__map = Map(map)
        self.__logger = logger.DiscontinousLog()
        self.__hour = 0


    # The method which is called by the simulation handler, this 
    # calls all the methods required and is representative of 
    # a day.
    def day(self, threadID):
        self.startTime = timeit.default_timer()
        self.__logger.log('day function', f'startTime: {self.startTime}, day: {self.__map.getDay()}')
        
        # anyone travelling to a quarinting place or coming from one 
        for pawn in [pawn for pawn in self.__map.getPopulation() if pawn.getArivalCheck()]:
            if self.__dbQueryHandler.getMapCannnotTravelTo(pawn.getStartingDestination())[0] == 1:
                pawn.setQuarantineTravelling()
                self.quarantine(pawn)
            pawn.setArivalCheck(0)
            self.__dbQueryHandler.updateArrivalCheck(pawn.getID(), pawn.getArivalCheck())

        # The 24 hour cycle 
        while self.__hour < 24:   
            self.__logger.log('day function whileloop', f'hour: {self.__hour}')

            # Checks if the number of infectectious infected is above a specified ammount for identify and isolate 
            # If it is then identify and isolate is set to true else false 
            if len(self.__dbQueryHandler.getInfectedInfectious(self.__map.getID())) >= self.__map.getIdentifyAndIsolateTriggerInfectionCount():
                self.isIdentiyIsolate = True 
            else:
                self.isIdentiyIsolate = False 
            
            # Checks if the number of infectious infected is above a specified ammount for limmiting travel
            # If it is then travel restrictions are set to true else false 
            if len(self.__dbQueryHandler.getInfectedInfectious(self.__map.getID())) >= self.__map.getTravelProhibitedTriggerInfectionCount():
                self.__dbQueryHandler.updateMapCannotTravelTo(self.__map.getID(), 1)
                self.travelRestirctions = True 
            else:
                self.__dbQueryHandler.updateMapCannotTravelTo(self.__map.getID(), 0)
                self.travelRestirctions = False 

            # check if infection time is over, if it is not then update infection time 
            self.startTime = timeit.default_timer()
            self.__logger.log('Started infected pawn function', f'hour: {self.__hour}')
            self.infPass()
            self.__logger.log('Finished infected pawn function',f'time taken: {timeit.default_timer() - self.startTime}')

            # update travelling
            self.startTime = timeit.default_timer()
            self.__logger.log('Started travelling function', f'hour: {self.__hour}')
            for pawn in self.__map.getPopulation():
                if pawn.getTravelling():
                    self.travelling(pawn)
            self.__logger.log('Finished travelling function',f'time taken: {timeit.default_timer() - self.startTime}')

            # movement
            self.startTime = timeit.default_timer()
            self.__logger.log('Started movement function', f'hour: {self.__hour}')
            self.movement()
            self.__logger.log('Finished movement function ',f'time taken: {timeit.default_timer() - self.startTime}')

            # transmission
            self.startTime = timeit.default_timer()
            self.__logger.log('Started transmission function', f'hour: {self.__hour}')
            for susceptiblePawn in self.tempoaryGroup(0, 'S'):
                if not susceptiblePawn.getTravelling() and not susceptiblePawn.getQuarantineTravelling():
                    self.transmission(susceptiblePawn)
            self.__logger.log('Finished transmission function',f'time taken: {timeit.default_timer() - self.startTime}')

            # update stats 
            self.startTime = timeit.default_timer()
            self.__logger.log('Started updating statistics function', f'hour: {self.__hour}')
            self.updateStatistics()
            self.__logger.log('Finished updating statistics function',f'time taken: {timeit.default_timer() - self.startTime}')
 
            # refreshes map with new pop 
            self.__map.populatePopulationFromDataBase(self.__map.getID())

            self.__hour +=1
            
        self.__logger.log('day function out of whileloop', f'hour: {self.__hour}')
        self.__map.updateDay()
        self.updateDB(1, threadID)
    

    # Checks over all the infected in the population and checks if they have 
    # passed a stage or are still on one (infectious, incubating)
    # updates values based on this as well as calling the identify and isolate method 
    # if identify and isolate is currently true 
    def infPass(self):
        infecetdGroup = self.tempoaryGroup(0 ,'I')
        if infecetdGroup != None:
                for infectedPawn in infecetdGroup:
                    if infectedPawn.getQuarantineInfected():
                        self.quarantine(infectedPawn)
                    elif infectedPawn.getIBtime() >= self.__disease.getIncubationTime(infectedPawn.getDiseaseId()):
                        infectedPawn.setIsIncubating(0)
                        infectedPawn.setIsInfectious(1)
                        if self.isIdentiyIsolate:
                            self.identify(infectedPawn)
                        elif infectedPawn.getItime() >= self.__disease.getInfectedTime(infectedPawn.getDiseaseId()):
                            infectedPawn.setIsInfectious(0)
                            infectedPawn.setDiseaseID(None)
                            infectedPawn.setStatus('R')
                        else:
                            infectedPawn.setIsInfectious(1)
                            infectedPawn.setItime()
                    else:
                        infectedPawn.setIsIncubating(1)
                        infectedPawn.setIBtime()


    def deathChance(self):
        pass


    def hospital(self):
        # capacity of hospital
        # number of hospitals
        # grade of hospital
        # when a pawn gets to a certain level of health they have a chance to go to hospital
        # ambulance get called out if the health is very low and if they are all busy then the pawn will die
        # chance for people to go to the hospital even if they don't need it if they have a high agitated tendancy
        pass


    # If a pawn is not already travelling then it sets all the variables up for it to
    # travel. If a pawn is travelling it checks if it has arrived and changes 
    # variables accordingly. If a map that a pawn is going to is blocking travel
    # then pawns are set to no longer travel to it 
    def travelling(self, pawn):
        if not pawn.getTravelling():
            if not self.travelRestirctions:
                newMapID = random.choice(self.__dbQueryHandler.getMapIDs(self.__map.getID()))[0]
                if self.__dbQueryHandler.getMapCannnotTravelTo(newMapID)[0] != 1:
                    pawn.setDestination(newMapID)
                    pawn.setTravelling(1)
                    self.__dbQueryHandler.updatePawnTravelling(pawn.getID(), pawn.getTravelling())
                    self.__dbQueryHandler.updatePawnDestination(pawn.getID(), newMapID)

        if pawn.getTravelling():
            if pawn.getTtime() >= self.__dbQueryHandler.getMapTravelTime(pawn.getDestination())[0]:
                # arrived
                pawn.setNTtime(0.0)
                pawn.setTtime(0.0)
                pawn.setTravelling(0)
                pawn.setID(pawn.getDestination())
                pawn.setArivalCheck(1)
                self.__dbQueryHandler.updatePawnTravelling(pawn.getID(), pawn.getTravelling())
                self.__dbQueryHandler.updatePawnPopulationID(pawn.getID(), pawn.getDestination())
                self.__dbQueryHandler.updatePawnDestination(pawn.getID(), None)
                self.__dbQueryHandler.updatePawnStatus(pawn.getID(), pawn.getStatus())
                self.__dbQueryHandler.updatePawnRtime(pawn.getID(), pawn.getRtime())
                self.__dbQueryHandler.updatePawnItime(pawn.getID(), pawn.getItime())
                self.__dbQueryHandler.updatePawnNTtime(pawn.getID(), pawn.getNTtime())
                self.__dbQueryHandler.updatePawnXPos(pawn.getID(), 0)
                self.__dbQueryHandler.updatePawnYPos(pawn.getID(),0)
                self.__dbQueryHandler.updateDiseaseID(pawn.getID(), pawn.getDiseaseId())
                self.__dbQueryHandler.updatePawnIBtime(pawn.getID(), pawn.getIBtime())
                self.__dbQueryHandler.updatePawnTtime(pawn.getID(), pawn.getTtime())
                self.__dbQueryHandler.updateArrivalCheck(pawn.getID(), pawn.getArivalCheck())
                self.__dbQueryHandler.updateIsInfectious(pawn.getID(), pawn.getIsInfectious())
                self.__dbQueryHandler.updateIsIncubating(pawn.getID(), pawn.getIsIncubating())
                self.__map.removePawn(pawn)
            else:
                if self.__dbQueryHandler.getMapCannnotTravelTo(pawn.getDestination())[0] != 0:
                    pawn.setDestination(None)
                    pawn.setTravelling(0)
                    pawn.setTtime(0.0)
                    self.__dbQueryHandler.updatePawnTravelling(pawn.getID(), pawn.getTravelling())
                    self.__dbQueryHandler.updatePawnDestination(pawn.getID(), pawn.getDestination())
                else:
                    pawn.setTtime()
 

    # Checks if a pawn is elligable to be quarantined 
    def identify(self, pawn):
        if pawn.getItime() >= self.__map.getInfectionTimeBeforeQuarantine() and pawn.getAsymptomatic() != 1:
            pawn.setQuarantineInfected()
            self.quarantine(pawn)
        else:
            pawn.setItime()
        
    # Updates or sets quartine for the pawn given 
    def quarantine(self, pawn):
        if pawn.getQuarantineInfected():
            if pawn.getItime() >= self.__disease.getInfectedTime(pawn.getDiseaseId()):
                pawn.setIsInfectious(0)
                pawn.setDiseaseID(None)
                pawn.setStatus('R')
                pawn.setQuarantineInfected(0)
                self.__dbQueryHandler.updateQinfected(pawn.getID(), pawn.getQuarantineInfected())
                self.__dbQueryHandler.updatePawnQtime(pawn.getID(), pawn.getQtime())
            else:
                pawn.setItime()
        elif pawn.getQuarantineTravelling():
            if pawn.getQtime() >= self.__map.getTravelQuarintineTime():
                pawn.setQuarantineTravelling(0)
                pawn.setQtime(0.0)
                self.__dbQueryHandler.updateQtravelling(pawn.getID(), pawn.getQuarantineTravelling())
                self.__dbQueryHandler.updatePawnQtime(pawn.getID(), pawn.getQtime())
            else:
                pawn.setQtime()


    # Updates the status of a pawn if they have been infected 
    def setStatus(self, susceptiblePawn, infectedPawn):
        diseaseID = infectedPawn.getDiseaseId()
        if random.random() < self.__dbQueryHandler.getGeneralMutationChance(0)[0]*self.__disease.getMutationChance(diseaseID):
            print('mutation')
            susceptiblePawn.setDiseaseID(self.diseaseMutation(infectedPawn.getID(), susceptiblePawn.getID(), infectedPawn.getDiseaseId()))
        else:
            susceptiblePawn.setDiseaseID(diseaseID)
        susceptiblePawn.setIBtime(0.0)
        susceptiblePawn.setStatus('I')
        if random.random() < self.__disease.getPasymptomatic(susceptiblePawn.getDiseaseId()):
            susceptiblePawn.setAsymptomatic(0)
        else: 
            susceptiblePawn.setAsymptomatic(1)


    # Checks if a susceptible pawn is in the transmissin radius of an infected pawn 
    # Then increases the radius time of the suscpetible pawn 
    # Once that is equal to or greater than the transmission time and a probablilty applied then the
    # susceptible pawn is set to infected.
    def transmission(self, susceptiblePawn):
        for infectedPawn in self.tempoaryGroup(2 ,'I') :
            if self.checkInsideRadius(infectedPawn.getPos()[0], infectedPawn.getPos()[1], susceptiblePawn.getPos()[0], susceptiblePawn.getPos()[1], infectedPawn.getDiseaseId()):
                if susceptiblePawn.getRtime() >= self.__disease.getTransmissionTime(infectedPawn.getDiseaseId()) and random.random() < P_INFECTION_PER_DAY * self.__disease.getContagion(infectedPawn.getDiseaseId()):
                    self.setStatus(susceptiblePawn, infectedPawn)
                    break
                else:
                    susceptiblePawn.setRtime()
                

    # Checks if a susceptible pawn is inside the transmission radius of an infected pawn 
    def checkInsideRadius(self, x1, y1, x2, y2, diseaseID) -> bool:  
        if (((x1 - x2)**2 + (y1 - y2)**2) <= self.__disease.getTransmissionRadius(diseaseID) * self.__disease.getTransmissionRadius(diseaseID)):
            return True 


    # maps have different ways to get to each other either driving which means no infection or flying which means the people on
    def movement(self):
        for pawn in self.tempoaryGroup(1 ,'R'):
            if not pawn.getTravelling():
                if pawn.getNTtime() >= self.__dbQueryHandler.getTimeRequiredBetweenTravels(0)[0] and self.__dbQueryHandler.getNumberOfMaps(0)[0] > 1:
                    if TRAVEL_RATE < random.random():
                        self.travelling(pawn)
                else:
                    pawn.setNTtime()
                    # x direction 
                    x_amount = random.randint(1, MAX_MOVE_AMOUNT)
                    self.checkMovement(0, self.__map.getWidth(), x_amount, pawn)
                    # y direction  
                    self.checkMovement(1, self.__map.getHeight(), random.randint(1, MAX_MOVE_AMOUNT) - x_amount, pawn)


    def checkMovement(self, direction, limit, moveAmount, pawn):
        if pawn.getPos()[direction] + moveAmount < limit:
            pawn.setPos(direction, moveAmount)
        elif pawn.getPos()[direction] - moveAmount > 0:
            pawn.setPos(direction, -moveAmount)


    def tempoaryGroup(self, type: int, st : str):
        if type == 0:
            return [pawn for pawn in self.__map.getPopulation() if pawn.getStatus() == st]
        elif type == 1:
            return [pawn for pawn in self.__map.getPopulation() if pawn.getStatus() != st]
        elif type == 2:
            return [pawn for pawn in self.__map.getPopulation() if pawn.getStatus() == st and pawn.getIBtime() >= self.__disease.getIncubationTime(pawn.getDiseaseId()) and not pawn.getQuarantineInfected()]


    def diseaseMutation(self, infectedID, susceptibleID, diseaseID):
        '''
        when a pawn first catches a disease chance for a mutaion to happen 
        disease id is going to be made up off day + infected id + susceptibleID + map name +  disease name
        name is going to be the disease name

        id                       STRING,
        name                     STRING,
        transmissionTime         FLOAT,
        contagion                FLOAT,
        transmissionRadius       INTEGER,
        infectedTime             FLOAT,
        incubationTime           FLOAT,
        ageMostSusceptible       INTEGER,
        virulence                INTEGER,
        pAsymptomaticOnInfection FLOAT,
        mutationChance           FLOAT
        
        '''

        newDiseaseID = f'{str(self.__map.getDay())}.{str(infectedID)}.{str(susceptibleID)}.{self.__map.getName()}.{self.__disease.getName(diseaseID)}'
        newD = [newDiseaseID, f'm{self.__disease.getName(diseaseID)}']
        oldDisease = self.__dbQueryHandler.getDiseaseMutation(diseaseID)[0][2:]
        for index, mutation in enumerate(MUTATIONS):
            for m in mutation:
                if m in ['int', 'float']:
                    type = m
                else:
                    effect = random.choice(m)[0]
            
            if type == 'float':
                change = random.uniform(0.0,0.2)

            elif type == 'int':
                change = random.randint(0,2)

            value = oldDisease[index]
            if random.random() < self.__disease.getMutationChance(diseaseID):
                if effect == '+':
                    value += change
                elif effect == '-':
                    value -= change
                if value < 0:
                    value = 0
            newD.append(value)
        self.__dbQueryHandler.createDisease(*newD)
        return newDiseaseID


    # merge update Statistics to this functon optimistation
    # update to add new data 
    def updateDB(self, type: int, threadID: int):
        for pawn in self.__map.getPopulation():
            self.__dbQueryHandler.updatePawnStatus(pawn.getID(), pawn.getStatus())
            self.__dbQueryHandler.updatePawnRtime(pawn.getID(), pawn.getRtime())
            self.__dbQueryHandler.updatePawnItime(pawn.getID(), pawn.getItime())
            self.__dbQueryHandler.updatePawnXPos(pawn.getID(), pawn.getPos()[0])
            self.__dbQueryHandler.updatePawnYPos(pawn.getID(), pawn.getPos()[1])
            self.__dbQueryHandler.updateDiseaseID(pawn.getID(), pawn.getDiseaseId())
            self.__dbQueryHandler.updatePawnIBtime(pawn.getID(), pawn.getIBtime())
            self.__dbQueryHandler.updatePawnTtime(pawn.getID(), pawn.getTtime())
            self.__dbQueryHandler.updatePawnNTtime(pawn.getID(), pawn.getNTtime())
            self.__dbQueryHandler.updateIsInfectious(pawn.getID(), pawn.getIsInfectious())
            self.__dbQueryHandler.updateIsIncubating(pawn.getID(), pawn.getIsIncubating())
            if pawn.getQuarantineTravelling() or pawn.getQuarantineInfected():
                self.__dbQueryHandler.updatePawnQtime(pawn.getID(), pawn.getQtime())
                self.__dbQueryHandler.updateQinfected(pawn.getID(), pawn.getQuarantineInfected())
                self.__dbQueryHandler.updateQtravelling(pawn.getID(), pawn.getQuarantineTravelling())

        self.__dbQueryHandler.updateMapDay(self.__map.getID(), self.__map.getDay())

        if type:
            self.updateStatistics()
            self.recordStatistics()
            self.__logger.log('finished database update', f'endTime: {timeit.default_timer()}')
            self.__logger.log('time taken', f'{timeit.default_timer() - self.startTime}')
            self.__logger.localDump(f'{threadID}')
            self.__dbQueryHandler.close()


    def updateStatistics(self):
        self.s,self.i,self.r = 0,0,0
        for pawn in self.__map.getPopulation():
            if not pawn.getTravelling() and not pawn.getQuarantineTravelling() and not pawn.getQuarantineInfected():
                if pawn.getStatus() == 'S':
                    self.s +=1
                elif pawn.getStatus() == 'I':
                    self.i +=1
                elif pawn.getStatus() == 'R':
                    self.r +=1
        
        self.__dbQueryHandler.updatePopulationSusceptible(self.__map.getID(),self.s)
        self.__dbQueryHandler.updatePopulationInfected(self.__map.getID(),self.i)
        self.__dbQueryHandler.updatePopulationRemoved(self.__map.getID(),self.r)


    def recordStatistics(self):
        fieldnames = ["day", "Susceptible", "Infected", "Removed"]
        with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/simData/{self.__map.getName()}data.csv'), 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
            info={
                "day" : self.__map.getDay(),
                "Susceptible" : self.s,
                "Infected" : self.i,
                "Removed" : self.r
            }
            csv_writer.writerow(info)


class Map:
    def __init__(self, map) -> None:
        self.__id = map[0]
        self.__name = map[1]
        self.__width = map[2]
        self.__height = map[3]
        self.__day = map[4]
        self.__govermentActionReliabilty = map[5]
        self.__identifyAndIsolateTriggerInfectionCount = map[6]
        self.__infectionTimeBeforeQuarantine = map[7]
        self.__travelQuarintineTime = map[8]
        self.__socialDistanceTriggerInfectionCount = map[9]
        self.__travelProhibitedTriggerInfectionCount = map[10]
        self.__population = self.populatePopulationFromDataBase(map[-1])
    

    def getName(self) -> str:
        return self.__name


    def getID(self) -> int:
        return self.__id


    def getWidth(self) -> int:
        return self.__width
    

    def getHeight(self) -> int:
        return self.__height


    def getDay(self) -> int:
        return self.__day


    def getGovermentActionReliabilty(self) -> float:
        return self.__govermentActionReliabilty


    def getIdentifyAndIsolateTriggerInfectionCount(self) -> int:
        return self.__identifyAndIsolateTriggerInfectionCount


    def getInfectionTimeBeforeQuarantine(self) -> float:
        return self.__infectionTimeBeforeQuarantine


    def getSocialDistanceTriggerInfectionCount(self) -> int:
        return self.__socialDistanceTriggerInfectionCount
    

    def getTravelQuarintineTime(self) -> float:
        return self.__travelQuarintineTime


    def getTravelProhibitedTriggerInfectionCount(self) -> int:
        return self.__travelProhibitedTriggerInfectionCount


    def getPopulation(self):
        return self.__population


    def removePawn(self, pawn):
        self.__population.pop(self.__population.index(pawn))


    def updateDay(self):
        self.__day += 1


    def populatePopulationFromDataBase(self, mapID):
        dbpopulation = dbH.DBManager(os.path.expanduser(FILE_PATH_DB)).getPopulation(mapID)
        dbH.DBManager(os.path.expanduser(FILE_PATH_DB)).close()
        return [Pawn(pawn[0], pawn[1], pawn[2], pawn[3], pawn[4], pawn[5], pawn[6], pawn[7], pawn[8], pawn[9], pawn[10], pawn[11], pawn[12], pawn[13], pawn[14], pawn[15], pawn[16], pawn[17], pawn[18], pawn[19], pawn[20], pawn[21], pawn[22], pawn[23]) for pawn in dbpopulation]


class Pawn:
    def __init__(self, id: int, status: str, rTime: float, iTime: float, ibTime: float, tTime: float, ntTime: float, travelling: int, asymptomatic: int, partialImmunity: float, startingDestination: int, destination: int,bloodType: str, age: int, health: float, posX: int, posY: int, qTime: float, qInfected: int, qTravelling: int, arrivalCheck: int, isInfectious: int, isIncubating: int, diseaseID: str) -> None:
        self.__iD = id
        self.__status = status
        self.__rTime = rTime
        self.__iTime = iTime
        self.__ibTime = ibTime
        self.__tTime = tTime
        self.__ntTime = ntTime
        self.__qTime = qTime
        self.__travelling = travelling
        self.__asymptomatic = asymptomatic
        self.__paritalImmunity = partialImmunity
        self.__destination = destination
        self.__startingDestination = startingDestination
        self.__bloodType = bloodType
        self.__age = age
        self.__health = health
        self.__quarantineInfected = qInfected
        self.__quarantineTravelling = qTravelling
        self.__arivalCheck = arrivalCheck
        self.__pos = [posX, posY]
        self.__isInfectious = isInfectious
        self.__isIncubating = isIncubating
        self.__diseaseID = diseaseID


    def getID(self) -> int:
        return self.__iD 


    def getStatus(self) -> str:
        return self.__status


    def getRtime(self) -> float:
        return self.__rTime


    def getItime(self) -> float:
        return self.__iTime


    def getIBtime(self) -> float:
        return self.__ibTime


    def getTtime(self) -> float:
        return self.__tTime


    def getQtime(self) -> float:
        return self.__qTime
    
    
    def getNTtime(self) -> float:
        return self.__ntTime


    def getTravelling(self) -> int:
        return self.__travelling


    def getStartingDestination(self) -> int:
        return self.__startingDestination


    def getDestination(self) -> int:
        return self.__destination


    def getArivalCheck(self) -> int:
        return self.__arivalCheck


    def getQuarantineInfected(self) -> int:
        return self.__quarantineInfected


    def getQuarantineTravelling(self) -> int:
        return self.__quarantineTravelling


    def getPos(self) -> list[int]:
        return self.__pos
    

    def getDiseaseId(self) -> str:
        return self.__diseaseID


    def getAsymptomatic(self) -> int:
        return self.__asymptomatic


    def getIsIncubating(self) -> int:
        return self.__isIncubating


    def getIsInfectious(self) -> int:
        return self.__isInfectious


    def setID(self, id: int) -> None:
        self.__iD = id


    def setStatus(self, st: str) -> None:
        self.__status = st


    def setItime(self, val: float = 1.0) -> None:
        self.__iTime += val/24.0

    
    def setRtime(self, val: float = 1.0) -> None:
        self.__rTime += val/24.0


    def setIBtime(self, val: float = 1.0) -> None:
        if self.__status == 'S':
            self.__ibTime = val
        else:
            self.__ibTime += val/24.0


    def setTtime(self, val: float =1.0) -> None:
        if self.__travelling:
            self.__tTime += val/24.0
        else:
            self.__tTime = val
    
    
    def setNTtime(self, val: float = 1.0) -> None:
        self.__ntTime += val/24.0


    def setQtime(self, val: float =1.0) -> None:
        if self.__quarantineTravelling:
            self.__qTime += val/24.0
        else:
            self.__qTime = val


    def setTravelling(self, val: int) -> None:
        self.__travelling = val 


    def setDestination(self, id: int) -> None:
        self.__destination = id


    def setArivalCheck(self, val: int) -> None:
        self.__arivalCheck = val


    def setPos(self, direction, moveAmount) -> None:
        self.__pos[direction] += moveAmount


    def setDiseaseID(self, diseaseID: int) -> None:
        self.__diseaseID = diseaseID
    

    def setQuarantineInfected(self, bool: int = 1) -> None:
        self.__quarantineInfected = bool

    
    def setQuarantineTravelling(self, bool: int = 1) -> None:
        self.__quarantineTravelling = bool


    def setAsymptomatic(self, bool: int) -> None:
        self.__asymptomatic = bool

    
    def setIsIncubating(self, bool: int = 1) -> None:
        self.__isIncubating = bool
    

    def setIsInfectious(self, bool: int = 1) -> None:
        self.__isInfectious = bool


# doesn't store anything only has getters and setters for the database so multiple disease can be around 
class Disease:
    def __init__(self, dbQuery) -> None:
        self.__dbQueryHandler = dbQuery
    

    def getName(self, id: str) -> str:
        return self.__dbQueryHandler.getDiseaseName(id)[0]

    
    def getTransmissionTime(self, id: str) -> float:
        return self.__dbQueryHandler.getDiseaseTransmissionTime(id)[0]
    

    def getContagion(self, id: str) -> float:
        return self.__dbQueryHandler.getDiseaseContagion(id)[0]
    

    def getTransmissionRadius(self, id: str) -> int:
        return self.__dbQueryHandler.getDiseaseTransmissionRadius(id)[0]
      

    def getInfectedTime(self, id: str) -> float:
        return self.__dbQueryHandler.getDiseaseInfectedTime(id)[0]
    

    def getIncubationTime(self, id: str) -> float:
        return self.__dbQueryHandler.getDiseaseIncubationTime(id)[0]
    

    def getPasymptomatic(self, id: str) -> float:
        return self.__dbQueryHandler.getDiseasetPasymptomatic(id)[0]

    
    def getMutationChance(self, id: str) -> float:
        return self.__dbQueryHandler.getDiseaseMutationChance(id)[0]

def getMutations():
    '''
    tuple with (+ and -)
    '''
    with open(os.path.expanduser(FILE_PATH_SETTINGS),'r') as file:
                data = json.load(file)
    for key in data['disease'][0]:
        if not key in ['name', 'numbBloodTypesSusceptible']:
            MUTATIONS.append([('+'+key,'-'+key),data['disease'][0][key][-1]])


getMutations()