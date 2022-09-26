import threading
import logger 
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

NUMB_PEOPLE = 20
NUMB_STARTING_INFECTED = 1


# Transform the main def into a class 
"""
simulation runs maps which contain population
"""
class Simulation:
    def __init__(self) -> None:
        self.__disease = createDisease()
        self.__map = createMap()
        self.__dayCounter = 0
    

    def setDayCounter(self):
        self.__dayCounter += 1


    def day(self):
        """
        need to choose the order of the day 
        """
        self.setDayCounter()
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
        return [person for person in self.__map.getPopulation() if person.getStatus() != st]


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
    def __init__(self, width, height, population) -> None:
        self.__width = width
        self.__height = height
        self.__population = population
    

    def getWidth(self) -> int:
        return self.__width
    

    def getHeight(self) -> int:
        return self.__height

    
    def getPopulation(self):
        return self.__population


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
    def __init__(self, iD: int,  s = 'S') -> None:
        self.iD = iD
        self.__status = s
        self.eRData = '' # either dead or immune 
        self.__rTime = 0
        self.__iTime = 0
        self.__pos = [random.randrange(WIDTH+1),random.randrange(HEIGHT+1)]


    def getPos(self):
        return self.__pos


    def getStatus(self):
        return self.__status


    def getItime(self):
        return self.__iTime


    def getRtime(self):
        return self.__rTime


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


def createMap():
    return Map(WIDTH, HEIGHT, createPopulation())


def createPopulation() -> list:
    population = []
    a = 0 
    for i in range(NUMB_PEOPLE):
        if a < NUMB_STARTING_INFECTED:
            population.append(Person(i+1, s='I'))
            a+=1
        else:
            population.append(Person(i+1))
    return population


def createDisease():
    return Disease(1,0.1,2,3)


log = logger.DiscontinousLog()
log.log('program start')
if __name__ == "__main__":
    running = True 
    sim = Simulation()
    while running:
        sim.day()
        sim.countStatistics()
        input('> ')

log.localDump('TASDAWD2')