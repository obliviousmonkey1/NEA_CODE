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
DEBUG = False

MAX_MOVE_AMOUNT = 2
MOVE_PROBABILITY = 0.5
MUTATION_CHANCE = 0.001
MOVE_CITY_CHANCE = 0.01

P = 1 # probablity ????


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

        if self.tempoaryGroup(0 ,'I'):
            while self.__hour < 24:
                self.__logger.log('day function whileloop', f'hour: {self.__hour}')
                infecetdGroup = self.tempoaryGroup(0 ,'I') 

                # check if infection time is over, if it is not then update infection time 
                if infecetdGroup != None:
                    for infectedPerson in infecetdGroup:
                        if infectedPerson.getIBtime() >= self.__disease.getIncubationTime(infectedPerson.getDiseaseId()):
                            if infectedPerson.getItime() >= self.__disease.getInfectedTime(infectedPerson.getDiseaseId()):
                                infectedPerson.setDiseaseID(None)
                                infectedPerson.setStatus('R')
                            else:
                                infectedPerson.setItime()
                        else:
                            infectedPerson.setIBtime()

                susceptibleGroup = self.tempoaryGroup(0, 'S')
                self.infecetdGroup = self.tempoaryGroup(0 ,'I') 

                self.movement()
                
                # split up suscpetible list into sub lists and then 
                # thread over them 
                # pool = Pool()
                # for susceptibleGroup in susceptibleGroups:
                    # pool.apply_async(self.infection, susceptibleGroup)
                for susceptiblePerson in susceptibleGroup:
                    self.infection(susceptiblePerson)
                
                self.__hour +=1

        self.__logger.log('day function out of whileloop', f'hour: {self.__hour}')
        self.__map.updateDay()
        self.updateStatistics()

        self.updateDB(threadID)
    

    def infection(self, susceptiblePerson):
        for infectedPerson in self.infecetdGroup:
            if self.checkInsideRadius(infectedPerson.getPos()[0], infectedPerson.getPos()[1], susceptiblePerson.getPos()[0], susceptiblePerson.getPos()[1], infectedPerson.getDiseaseId()):
                if susceptiblePerson.getRtime() >= self.__disease.getTransmissionTime(infectedPerson.getDiseaseId()) and random.random() < P * self.__disease.getContagion(infectedPerson.getDiseaseId()):
                    if random.random() < MUTATION_CHANCE:
                        susceptiblePerson.setDiseaseID(self.diseaseMutation(infectedPerson.getID(), susceptiblePerson.getID(), infectedPerson.getDiseaseId()))
                    else:
                        susceptiblePerson.setDiseaseID(infectedPerson.getDiseaseId())
                    susceptiblePerson.setIBtime(0.0)
                    susceptiblePerson.setStatus('I')
                else:
                    susceptiblePerson.setRtime()


    def checkInsideRadius(self, x, y, c_x, c_y, diseaseID) -> bool:  
        if ((x - c_x) * (x - c_x) + (y - c_y) * (y - c_y) <= self.__disease.getTransmissionRadius(diseaseID) * self.__disease.getTransmissionRadius(diseaseID)):
            return True 


    # maps have different ways to get to each other either driving which means no infection or flying which means the people on
    # the same flight as an infected person will have the time tick up 
    def movement(self):
        """
        x change:
            Random number between 0 and MAX_MOV_AMMOUNT,
            Then check poitive and negative direction if one is outbound pick the other one if both in bounds
            then random pick between them. (checked with the change added to the current value)
        y change: 
            Random number between 0 and MAX_MOV_AMMOUNT - pos(x change)
            Then check poitive and negative direction if one is outbound pick the other one if both in bounds
            then random pick between them.  (checked with the change added to the current value)
        Add those values to the current values 
        """
        notR_group = self.tempoaryGroup(1 ,'R')
        if random.random() < MOVE_CITY_CHANCE:
            pass
        if random.random() < MOVE_PROBABILITY:
            for person in notR_group:
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
    def updateDB(self, threadID):
        for person in self.__map.getPopulation():
            self.__dbQueryHandler.updatePersonStatus(person.getID(), person.getStatus())
            self.__dbQueryHandler.updatePersonRtime(person.getID(), person.getRtime())
            self.__dbQueryHandler.updatePersonItime(person.getID(), person.getItime())
            self.__dbQueryHandler.updatePersonXPos(person.getID(), person.getPos()[0])
            self.__dbQueryHandler.updatePersonYPos(person.getID(), person.getPos()[1])
            self.__dbQueryHandler.updateDiseaseID(person.getID(), person.getDiseaseId())
            self.__dbQueryHandler.updatePersonIBtime(person.getID(), person.getIBtime())
        self.__dbQueryHandler.updateMapDay(self.__map.getID(), self.__map.getDay())

        print(self.__dbQueryHandler.getMapDay(self.__map.getID()))
        self.__dbQueryHandler.close()
        self.recordStatistics()
        self.__logger.log('finished database update', f'endTime: {timeit.default_timer()}')
        self.__logger.log('time taken', f'{timeit.default_timer() - self.startTime}')
        self.__logger.localDump(f'{threadID}')
        return [self.__map.getID, self.__map.getDay, self.s,self.i,self.r]


    def updateStatistics(self):
        self.s,self.i,self.r = 0,0,0
        for person in self.__map.getPopulation():
            if person.getStatus() == 'S':
                self.s +=1
            elif person.getStatus() == 'I':
                self.i +=1
            elif person.getStatus() == 'R':
                self.r +=1

    def recordStatistics(self):
        try:
            fieldnames = ["day", "Susceptible", "Infected", "Removed"]
            with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/{self.__map.getName()}data.csv'), 'w') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
            
            with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/{self.__map.getName()}data.csv'), 'a') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
                info={
                    "day" : self.__map.getDay(),
                    "Susceptible" : self.s,
                    "Infected" : self.i,
                    "Removed" : self.r
                }
                csv_writer.writerow(info)

        except:
            with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/{self.__map.getName()}data.csv'), 'a') as csv_file:
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
        self.__population = self.populatePopulationFromDataBase(map[0])
    

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

    
    def getPopulation(self):
        return self.__population


    def updateDay(self):
        self.__day += 1


    def populatePopulationFromDataBase(self, mapID):
        dbpopulation = dbH.DBManager(os.path.expanduser(FILE_PATH_DB)).getPopulation(mapID)
        dbH.DBManager(os.path.expanduser(FILE_PATH_DB)).close()
        return [Person(person[0], person[1], person[2], person[3], person[4], person[5], person[6], person[10]) for person in dbpopulation]


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


class Person:
    def __init__(self, id: int, status: str, rTime: float, iTime: float, ibTime: float, posX: int, posY: int, diseaseID: str) -> None:
        self.__iD = id
        self.__status = status
        self.__rTime = rTime
        self.__iTime = iTime
        self.__ibTime = ibTime
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


    def getPos(self) -> list[int]:
        return self.__pos
    

    def getDiseaseId(self) -> str:
        return self.__diseaseID


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


    def setPos(self, direction, moveAmount) -> None:
        self.__pos[direction] += moveAmount


    def setDiseaseID(self, diseaseID: int)-> None:
        self.__diseaseID = diseaseID

