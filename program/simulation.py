FILE_PATH_DBH = '~/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_DB = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'
FILE_PATH_LOG = '~/Documents/NEA/NEA_CODE/program/inhouse tools'

import sys
import os
sys.path.append(os.path.expanduser(FILE_PATH_LOG))
sys.path.append(os.path.expanduser(FILE_PATH_DBH))

import dbHandler as dbH
import logger  
from multiprocessing import Pool
import random
import timeit
import csv 

'''
S - Susceptible
I - Infected
R - Removed
people randomly move about map and if they are within the area of contagion of an infected person for 
x amount of time they become infected SIR model 

NEED TO ADD :

    should add death chance 
    need to add identify and isolate features 
    socal distancing
    travel restrictions
    r
    central hubs

NEED TO WORK OUT THREAD DEADLOCK FOR DATABASE

'''

# Constants 
MAX_MOVE_AMOUNT = 2
MOVE_PROBABILITY = 0.5
MUTATION_CHANCE = 0.001
TRAVEL_RATE = 0.99
P_INFECTION_PER_DAY = 1 
NT_TIME = 1.0


class Simulation:
    def __init__(self, map) -> None:
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))
        self.__disease = Disease(self.__dbQueryHandler)
        self.__map = Map(map)
        self.__logger = logger.DiscontinousLog()
        self.__hour = 0


    # need to brake up day into sub functions 
    # need to use continous log
    def day(self, threadID):
        self.startTime = timeit.default_timer()
        self.__logger.log('day function', f'startTime: {self.startTime}, day: {self.__map.getDay()}')
        
        for person in [person for person in self.__map.getPopulation() if person.getArivalCheck()]:
            if self.__dbQueryHandler.getPopulationInfected(self.__map.getID())[0] >= self.__map.getIdentifyAndIsolateTriggerInfectionCount():
                person.setQtime()
                self.quarantine()
            person.setArivalCheck(0)

        if self.tempoaryGroup(0 ,'I'):
            while self.__hour < 24:   
                self.__logger.log('day function whileloop', f'hour: {self.__hour}')

                if self.__dbQueryHandler.getPopulationInfected(self.__map.getID())[0] >= self.__map.getIdentifyAndIsolateTriggerInfectionCount():
                    self.isIdentiyIsolate = True 
                else:
                    self.isIdentiyIsolate = False 
                
                if self.__dbQueryHandler.getPopulationInfected(self.__map.getID())[0] >= self.__map.getTravelProhibitedTriggerInfectionCount():
                    print('set cannot travel to 1')
                    self.__dbQueryHandler.updateMapCannotTravelTo(self.__map.getID(), 1)
                else:
                    self.__dbQueryHandler.updateMapCannotTravelTo(self.__map.getID(), 0)

                # check if infection time is over, if it is not then update infection time 
                self.startTime = timeit.default_timer()
                self.__logger.log('Started infected person function', f'hour: {self.__hour}')
                self.infPass()
                self.__logger.log('Finished infected person function',f'time taken: {timeit.default_timer() - self.startTime}')

                # update travelling
                self.startTime = timeit.default_timer()
                self.__logger.log('Started travelling function', f'hour: {self.__hour}')
                for person in self.__map.getPopulation():
                    if person.getTravelling():
                        self.travelling(person)
                self.__logger.log('Finished travelling function',f'time taken: {timeit.default_timer() - self.startTime}')

                # movement
                self.startTime = timeit.default_timer()
                self.__logger.log('Started movement function', f'hour: {self.__hour}')
                self.movement()
                self.__logger.log('Finished movement function ',f'time taken: {timeit.default_timer() - self.startTime}')

                # transmission
                self.startTime = timeit.default_timer()
                self.__logger.log('Started transmission function', f'hour: {self.__hour}')
                for susceptiblePerson in self.tempoaryGroup(0, 'S'):
                    if not susceptiblePerson.getTravelling():
                        self.transmission(susceptiblePerson)
                self.__logger.log('Finished transmission function',f'time taken: {timeit.default_timer() - self.startTime}')

                # update stats 
                self.startTime = timeit.default_timer()
                self.__logger.log('Started updating statistics function', f'hour: {self.__hour}')
                self.updateStatistics()
                self.__logger.log('Finished updating statistics function',f'time taken: {timeit.default_timer() - self.startTime}')

                #self.updateDB(0, threadID)
                # refreshes map with new pop 
                self.__map.populatePopulationFromDataBase(self.__map.getID())

                self.__hour +=1

        self.__logger.log('day function out of whileloop', f'hour: {self.__hour}')
        self.__map.updateDay()
        self.updateDB(1, threadID)
    

    def infPass(self):
        infecetdGroup = self.tempoaryGroup(0 ,'I')
        if infecetdGroup != None:
                for infectedPerson in infecetdGroup:
                    if infectedPerson.getIBtime() >= self.__disease.getIncubationTime(infectedPerson.getDiseaseId()):
                        if self.isIdentiyIsolate:
                            self.identify(infectedPerson)
                        if infectedPerson.getItime() >= self.__disease.getInfectedTime(infectedPerson.getDiseaseId()):
                            infectedPerson.setDiseaseID(None)
                            infectedPerson.setStatus('R')
                        else:
                            infectedPerson.setItime()
                    else:
                        infectedPerson.setIBtime()


    def travelling(self, person):
        if not person.getTravelling():
            newMapID = random.choice(self.__dbQueryHandler.getMapIDs(self.__map.getID()))[0]
            if self.__dbQueryHandler.getMapCannnotTravelTo(newMapID)[0] != 1:
                person.setDestination(newMapID)
                person.setTravelling(1)
                self.__dbQueryHandler.updatePersonTravelling(person.getID(), person.getTravelling())
                self.__dbQueryHandler.updatePersonDestination(person.getID(), newMapID)

        if person.getTravelling():
            if person.getTtime() >= self.__dbQueryHandler.getMapTravelTime(person.getDestination())[0]:
                # quarintine 
                person.setNTtime(0.0)
                person.setTtime(0.0)
                person.setTravelling(0)
                person.setID(person.getDestination())
                person.setArivalCheck(1)
                self.__dbQueryHandler.updatePersonTravelling(person.getID(), person.getTravelling())
                self.__dbQueryHandler.updatePersonPopulationID(person.getID(), person.getDestination())
                self.__dbQueryHandler.updatePersonDestination(person.getID(), None)
                self.__dbQueryHandler.updatePersonStatus(person.getID(), person.getStatus())
                self.__dbQueryHandler.updatePersonRtime(person.getID(), person.getRtime())
                self.__dbQueryHandler.updatePersonItime(person.getID(), person.getItime())
                self.__dbQueryHandler.updatePersonXPos(person.getID(), 0)
                self.__dbQueryHandler.updatePersonYPos(person.getID(),0)
                self.__dbQueryHandler.updateDiseaseID(person.getID(), person.getDiseaseId())
                self.__dbQueryHandler.updatePersonIBtime(person.getID(), person.getIBtime())
                self.__dbQueryHandler.updatePersonTtime(person.getID(), person.getTtime())
                self.__map.removePerson(person)
            else:
                if self.__dbQueryHandler.getMapCannnotTravelTo(person.getDestination())[0] != 0:
                    # print('cant travel')
                    person.setDestination(None)
                    person.setTravelling(0)
                    person.setTtime(0.0)
                    self.__dbQueryHandler.updatePersonTravelling(person.getID(), person.getTravelling())
                    self.__dbQueryHandler.updatePersonDestination(person.getID(), person.getDestination())
                else:
                    # print(f'set t time : {self.__dbQueryHandler.getMapCannnotTravelTo(person.getDestination())[0]}, map id {self.__map.getID()}')
                    person.setTtime()


    def identify(self, person):
        if person.getItime() >= self.__map.getInfectionTimeBeforeQuarantine() and person.getAsymptomatic() != 1:
            self.quarantine(person)
        # chance to not identify infected people 
        # if numbCases == criticalThresholdOfCases:
        #     if person.getNumbDaysInfected == quarantineDayAfterInfection:
        #         self.quarantine(person)
        #     elif ((person.getLastMapID != map.getMapID) and (person.getDaysSpent =< quarantineSusceptibleDays)):
        #         self.quarantine(person)
        
       
    def quarantine(self,person):
        if person.getQuarantineInfected():
            if person.getItime() >= self.__disease.getInfectedTime(person.getDiseaseId()):
                person.setDiseaseID(None)
                person.setStatus('R')
                person.setQuarantineInfected(0)
            else:
                person.setItime()
        elif person.getQuarantineTravelling():
            if person.getQtime() >= self.__map.getTravelQuarantineTime():
                person.setQuarantineTravelling(0)
                person.setQtime(0.0)
            else:
                person.setQtime()


    def setStatus(self, susceptiblePerson, infectedPerson):
        diseaseID = infectedPerson.getDiseaseId()
        # if random.random() < MUTATION_CHANCE:
        #     susceptiblePerson.setDiseaseID(self.diseaseMutation(infectedPerson.getID(), susceptiblePerson.getID(), infectedPerson.getDiseaseId()))
        # else:
        #     susceptiblePerson.setDiseaseID(infectedPerson.getDiseaseId())
        susceptiblePerson.setDiseaseID(diseaseID)
        susceptiblePerson.setIBtime(0.0)
        susceptiblePerson.setStatus('I')
        if random.random() < self.__disease.getPasymptomatic(diseaseID):
            susceptiblePerson.setAsymptomatic(0)
        else: 
            susceptiblePerson.setAsymptomatic(1)


    def transmission(self, susceptiblePerson):
        for infectedPerson in self.tempoaryGroup(2 ,'I') :
            if self.checkInsideRadius(infectedPerson.getPos()[0], infectedPerson.getPos()[1], susceptiblePerson.getPos()[0], susceptiblePerson.getPos()[1], infectedPerson.getDiseaseId()):
                if susceptiblePerson.getRtime() >= self.__disease.getTransmissionTime(infectedPerson.getDiseaseId()) and random.random() < P_INFECTION_PER_DAY * self.__disease.getContagion(infectedPerson.getDiseaseId()):
                    self.setStatus(susceptiblePerson, infectedPerson)
                    break
                else:
                    susceptiblePerson.setRtime()
                

    def checkInsideRadius(self, x1, y1, x2, y2, diseaseID) -> bool:  
        if (((x1 - x2)**2 + (y1 - y2)**2) <= self.__disease.getTransmissionRadius(diseaseID) * self.__disease.getTransmissionRadius(diseaseID)):
            return True 


    # maps have different ways to get to each other either driving which means no infection or flying which means the people on
    # the same flight as an infected person will have the time tick up 
    def movement(self):
        for person in self.tempoaryGroup(1 ,'R'):
            if not person.getTravelling():
                print(person.getTravelling())
                print(person.getNTtime())
                if person.getNTtime() >= NT_TIME:
                    if TRAVEL_RATE < random.random():
                        self.travelling(person)
                else:
                    person.setNTtime()
                    # x direction 
                    x_amount = random.randint(1, MAX_MOVE_AMOUNT)
                    self.checkMovement(0, self.__map.getWidth(), x_amount, person)
                    # y direction  
                    self.checkMovement(1, self.__map.getHeight(), random.randint(1, MAX_MOVE_AMOUNT) - x_amount, person)


    def checkMovement(self, direction, limit, moveAmount, person):
        if person.getPos()[direction] + moveAmount < limit:
            person.setPos(direction, moveAmount)
        elif person.getPos()[direction] - moveAmount > 0:
            person.setPos(direction, -moveAmount)


    def tempoaryGroup(self, type: int, st : str):
        if type == 0:
            return [person for person in self.__map.getPopulation() if person.getStatus() == st]
        elif type == 1:
            return [person for person in self.__map.getPopulation() if person.getStatus() != st]
        elif type == 2:
            return [person for person in self.__map.getPopulation() if person.getStatus() == st and person.getIBtime() >= self.__disease.getIncubationTime(person.getDiseaseId())]


    def diseaseMutation(self, infectedID, susceptibleID, diseaseID):
        '''
        when a person first catches a disease chance for a mutaion to happen 
        disease id is going to be made up off day + infected id + susceptibleID + map name +  disease name
        name is going to be the disease name
        '''
        newDiseaseID = f'{str(self.__map.getDay())}.{str(infectedID)}.{str(susceptibleID)}.{self.__map.getName()}.{self.__disease.getName(diseaseID)}'
        self.__dbQueryHandler.createDisease(
            newDiseaseID, f'm{self.__disease.getName(diseaseID)}', self.__disease.getTransmissionTime(diseaseID),
            self.__disease.getContagion(diseaseID), self.__disease.getTransmissionRadius(diseaseID),
            self.__disease.getInfectedTime(diseaseID), self.__disease.getIncubationTime(diseaseID)
        )
        return newDiseaseID


    # merge update Statistics to this functon optimistation
    # update to add new data 
    def updateDB(self, type: int, threadID: int):
        for person in self.__map.getPopulation():
            self.__dbQueryHandler.updatePersonStatus(person.getID(), person.getStatus())
            self.__dbQueryHandler.updatePersonRtime(person.getID(), person.getRtime())
            self.__dbQueryHandler.updatePersonItime(person.getID(), person.getItime())
            self.__dbQueryHandler.updatePersonXPos(person.getID(), person.getPos()[0])
            self.__dbQueryHandler.updatePersonYPos(person.getID(), person.getPos()[1])
            self.__dbQueryHandler.updateDiseaseID(person.getID(), person.getDiseaseId())
            self.__dbQueryHandler.updatePersonIBtime(person.getID(), person.getIBtime())
            self.__dbQueryHandler.updatePersonTtime(person.getID(), person.getTtime())
            self.__dbQueryHandler.updatePersonNTtime(person.getID(), person.getNTtime())
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
        for person in self.__map.getPopulation():
            if person.getStatus() == 'S':
                self.s +=1
            elif person.getStatus() == 'I':
                self.i +=1
            elif person.getStatus() == 'R':
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
        self.__socialDistanceTriggerInfectionCount = map[8]
        self.__travelProhibitedTriggerInfectionCount = map[9]
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
    

    def getTravelProhibitedTriggerInfectionCount(self) -> int:
        return self.__travelProhibitedTriggerInfectionCount


    def getPopulation(self):
        return self.__population


    def removePerson(self, person):
        self.__population.pop(self.__population.index(person))


    def updateDay(self):
        self.__day += 1


    def populatePopulationFromDataBase(self, mapID):
        dbpopulation = dbH.DBManager(os.path.expanduser(FILE_PATH_DB)).getPopulation(mapID)
        dbH.DBManager(os.path.expanduser(FILE_PATH_DB)).close()
        return [Person(person[0], person[1], person[2], person[3], person[4], person[5], person[6], person[7], person[8], person[9], person[10], person[11], person[12], person[13], person[14],person[15],person[16],person[17], person[18],person[19],person[20]) for person in dbpopulation]


class Person:
    def __init__(self, id: int, status: str, rTime: float, iTime: float, ibTime: float, tTime: float, ntTime: float, travelling: int, asymptomatic: int, partialImmunity: float, destination: int,bloodType: str, age: int, health: float, posX: int, posY: int, qTime: float, qInfected: int, qTravelling: int, arrivalCheck: int, diseaseID: str) -> None:
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
        self.__bloodType = bloodType
        self.__age = age
        self.__health = health
        self.__quarantineInfected = qInfected
        self.__quarantineTravelling = qTravelling
        self.__arivalCheck = arrivalCheck
        self.__pos = [posX, posY]
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
    

    def setAsymptomatic(self, bool: int) -> None:
        self.__asymptomatic = bool


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