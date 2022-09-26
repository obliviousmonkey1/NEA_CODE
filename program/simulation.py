import sys
sys.path.append('/Users/parzavel/Documents/NEA/NEA_CODE/program/inhouse tools')
sys.path.append('/Users/parzavel/Documents/NEA/NEA_CODE/program/database')

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

WIDTH = 5
HEIGHT = 5

MAX_MOVE_AMOUNT = 2
MOVE_PROB = 0.5

P = 1 # probablity ????


class Simulation:
    def __init__(self, map) -> None:
        self.__disease = createDisease()
        self.__map = Map(map)
        self.__dbQueryHandler = dbH.DBManager('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db')


    def day(self):
        """
        need to choose the order of the day 
        """
        self.__map.getDay()
        self.movement()

        s_group = self.tempoaryGroup(0, 'S')
        i_group = self.tempoaryGroup(0 ,'I') 

        for i_person in i_group:
            i_person.setItime()

        for s_person in s_group:
            for i_person in i_group:
                if self.checkInsideRadius(i_person.getPos()[0], i_person.getPos()[1], s_person.getPos()[0], s_person.getPos()[1]):
                    s_person.setRtime()
                    if s_person.getRtime() >= self.__disease.getTransmissionTime() and random.random() < P * self.__disease.getDiseaseTransmission():
                        s_person.setStatus('I')
            
        for i_person in i_group:
            if i_person.getItime() > self.__disease.getInfectedTime():
                i_person.setStatus('R')
        
        self.movement()
        self.updateDB()


    def checkInsideRadius(self, x, y, c_x, c_y) -> bool:  
        if ((x - c_x) * (x - c_x) + (y - c_y) * (y - c_y) <= self.__disease.getTransmissionRadius() * self.__disease.getTransmissionRadius()):
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


    def updateDB(self):
        for person in self.__map.getPopulation():
            self.__dbQueryHandler.updatePersonStatus(person.getID(), person.getStatus())
            self.__dbQueryHandler.updatePersonRtime(person.getID(), person.getRtime())
            self.__dbQueryHandler.updatePersonItime(person.getID(), person.getItime())
            self.__dbQueryHandler.updatePersonXPos(person.getID(), person.getPos()[0])
            self.__dbQueryHandler.updatePersonYPos(person.getID(), person.getPos()[1])
        self.__dbQueryHandler.updateMapDay(self.__map.getID(), self.__map.getDay())


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
        self.__width = map[2]
        self.__height = map[3]
        self.__day = map[4]
        self.__population = self.populatePopulationFromDataBase(map[0])
    

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
        dbpopulation = dbH.DBManager('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db').getPopulation(mapID)
        dbH.DBManager('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db').close()
        return [Person(person[0], person[1], person[2], person[3], person[4], person[5]) for person in dbpopulation]


class Disease:
    def __init__(self, tT, dT, tR, iT) -> None:
        self.__transmissionTime = tT
        self.__diseaseTransmission = dT
        self.__transmissionRadius = tR
        self.__infectedTime = iT

    
    def getTransmissionTime(self):
        return self.__transmissionTime
    

    def getDiseaseTransmission(self):
        return self.__diseaseTransmission
    

    def getTransmissionRadius(self):
        return self.__transmissionRadius


    def getInfectedTime(self):
        return self.__infectedTime


class Person:
    def __init__(self, id: int, status: str, rTime: int, iTime: int, posX: int, posY: int) -> None:
        self.__iD = id
        self.__status = status
        self.__rTime = rTime
        self.__iTime = iTime
        self.__pos = [posX, posY]


    def getID(self) -> int:
        return self.__iD 


    def getStatus(self):
        return self.__status


    def getRtime(self):
        return self.__rTime


    def getItime(self):
        return self.__iTime


    def getPos(self) -> list[int]:
        return self.__pos
    

    # check if this is good programming should i have called getPos or since its in the player should i just directly access it 
    def setPos(self, direction, moveAmount):
        self.__pos[direction] += moveAmount


    def setStatus(self, st: str):
        self.__status = st


    def setItime(self, mod=0):
        self.__iTime += 1+mod

    
    def setRtime(self, mod=0):
        self.__rTime += 1+mod


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


def createDisease():
    return Disease(1,0.1,2,3)
