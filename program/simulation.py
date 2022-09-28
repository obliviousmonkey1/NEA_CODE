FILE_PATH_DBH = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_DB = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db'
FILE_PATH_LOG = '/Users/parzavel/Documents/NEA/NEA_CODE/program/inhouse tools'

import sys
sys.path.append(FILE_PATH_LOG)
sys.path.append(FILE_PATH_DBH)

import dbHandler as dbH
import logger  
import threading
import random
from itertools import count 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

'''
very naive model

S - Susceptible
I - Infected
R - Removed
people randomly move about map and if they are within the area of contagion of an infected person for 
x amount of time they become infected SIR model 

should add death chance 

USE THREADING IN ORDER TO SPLIT 
UP THE LIST OF PEOPLE INTO SECTIONS SO THAT THE CHECKING IF A PERSON IS IN AN 
INFECTION AREA IS QUICKER, YOU COULD HAVE THE NUMBER OF THREADS, AND THEIRFORE THE 
MORE SPLIT THE LIST TIE INTO THE NUMBER OF PEOPLE USED.

NEED TO ADD GETTERS AND SETTERS
'''

# Constants 
DEBUG = False

MAX_MOVE_AMOUNT = 2
MOVE_PROB = 0.5
MUTATION_CHANCE = 0.3

P = 1 # probablity ????


# run on a 24 hour basis 
class Simulation:
    def __init__(self, map) -> None:
        self.__dbQueryHandler = dbH.DBManager(FILE_PATH_DB)
        self.__disease = Disease(self.__dbQueryHandler)
        self.__map = Map(map)
        self.__hour = 0


    # need to brake up day into sub functions 
    def day(self, threadID):
        """
        need to choose the order of the day 
        need to update to run on an hour basis so need to change the infection checking stuff and setting of Itime()
        """
        while self.__hour < 24:
            #print(self.__hour, threadID)
            infecetdGroup = self.tempoaryGroup(0 ,'I') 

            # check if infection time is over, if it is not then update infection time 
            if infecetdGroup != None:
                for infectedPerson in infecetdGroup:
                    if infectedPerson.getItime() >= self.__disease.getInfectedTime(infectedPerson.getDiseaseId()):
                        infectedPerson.setDiseaseID(None)
                        infectedPerson.setStatus('R')
                    else:
                        infectedPerson.setItime()

            susceptibleGroup = self.tempoaryGroup(0, 'S')
            infecetdGroup = self.tempoaryGroup(0 ,'I') 

            self.movement()

            for susceptiblePerson in susceptibleGroup:
                for infectedPerson in infecetdGroup:
                    if self.checkInsideRadius(infectedPerson.getPos()[0], infectedPerson.getPos()[1], susceptiblePerson.getPos()[0], susceptiblePerson.getPos()[1], infectedPerson.getDiseaseId()):
                        susceptiblePerson.setRtime()
                        if susceptiblePerson.getRtime() >= self.__disease.getTransmissionTime(infectedPerson.getDiseaseId()) and random.random() < P * self.__disease.getContagion(infectedPerson.getDiseaseId()):
                            if random.random() < MUTATION_CHANCE:
                                susceptiblePerson.setDiseaseID(self.diseaseMutation(infectedPerson.getID(), susceptiblePerson.getID(), infectedPerson.getDiseaseId()))
                            else:
                                susceptiblePerson.setDiseaseID(infectedPerson.getDiseaseId())
                            susceptiblePerson.setStatus('I')
            
            self.__hour +=1

        # update day and update database with new values 
        self.__map.updateDay()
        self.updateDB()


    def checkInsideRadius(self, x, y, c_x, c_y, diseaseID) -> bool:  
        if ((x - c_x) * (x - c_x) + (y - c_y) * (y - c_y) <= self.__disease.getTransmissionRadius(diseaseID) * self.__disease.getTransmissionRadius(diseaseID)):
            return True 


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
        if random.random() < MOVE_PROB:
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
        disease id is going to be made up off day + infected id + susceptibleID + map name + og disease id
        name is going to be the disease name
        '''
        ndID = f'{str(self.__map.getDay())}.{str(infectedID)}.{str(susceptibleID)}.{self.__map.getName()}.{str(diseaseID)}'
        print(ndID)
        self.__dbQueryHandler.createDisease(
            ndID, f'm{self.__disease.getName(diseaseID)}', self.__disease.getTransmissionTime(diseaseID),
            self.__disease.getContagion(diseaseID), self.__disease.getTransmissionRadius(diseaseID),
            self.__disease.getInfectedTime(diseaseID)
        )
        return ndID


    def updateDB(self):
        for person in self.__map.getPopulation():
            self.__dbQueryHandler.updatePersonStatus(person.getID(), person.getStatus())
            self.__dbQueryHandler.updatePersonRtime(person.getID(), person.getRtime())
            self.__dbQueryHandler.updatePersonItime(person.getID(), person.getItime())
            self.__dbQueryHandler.updatePersonXPos(person.getID(), person.getPos()[0])
            self.__dbQueryHandler.updatePersonYPos(person.getID(), person.getPos()[1])
            self.__dbQueryHandler.updateDiseaseID(person.getID(), person.getDiseaseId())
        self.__dbQueryHandler.updateMapDay(self.__map.getID(), self.__map.getDay())
        print(self.__dbQueryHandler.getMapDay(self.__map.getID()))
        self.__dbQueryHandler.close()


    def countStatistics(self):
        s,i,r = 0,0,0
        for person in self.__map.getPopulation():
            if person.getStatus() == 'S':
                s +=1
            elif person.getStatus() == 'I':
                i +=1
            elif person.getStatus() == 'R':
                r +=1
        print('s - ', end="")
        print(s)
        print('i - ', end="")
        print(i)
        print('r - ', end="")
        print(r)


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
        dbpopulation = dbH.DBManager(FILE_PATH_DB).getPopulation(mapID)
        dbH.DBManager(FILE_PATH_DB).close()
        return [Person(person[0], person[1], person[2], person[3], person[4], person[5], person[6]) for person in dbpopulation]


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


class Person:
    def __init__(self, id: int, status: str, rTime: float, iTime: float, posX: int, posY: int, diseaseID: str) -> None:
        self.__iD = id
        self.__status = status
        self.__rTime = rTime
        self.__iTime = iTime
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


    def getPos(self) -> list[int]:
        return self.__pos
    

    def getDiseaseId(self) -> str:
        return self.__diseaseID


    def setPos(self, direction, moveAmount) -> None:
        self.__pos[direction] += moveAmount


    def setStatus(self, st: str) -> None:
        self.__status = st


    def setItime(self, val: float = 1.0) -> None:
        self.__iTime += val/24.0

    
    def setRtime(self, val: float = 1.0) -> None:
        self.__rTime += val/24.0


    def setDiseaseID(self, diseaseID: int)-> None:
        self.__diseaseID = diseaseID


    def display_stats(self):
        print(f''' 
        ID : {self.iD}
        Data :
            - status : {self.status}
            - eRData : {self.eRData}
            - rTime : {self.rTime}
            - iTime : {self.iTime}
            - pos : {self.pos}
        ''')
