from msilib.schema import Class
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

T_TIME = 1 # in hours 
T_RADIUS = 2 # radius 
WIDTH = 5
HEIGHT = 5

MAX_MOVE_AMOUNT = 2
MOVE_PROB = 0.5

P = 1 # probablity ????
DT = 0.1 # disease transmission
INFECTION_TOTAL_TIME = 3 # day

NUMB_PEOPLE = 20
NUMB_STARTING_INFECTED = 1


# Transform the main def into a class 
class Simulation:
    def __init__(self) -> None:
        self.disease = create_disease()
        self.population = create_population()
        self.day = 0


class Disease:
    def __init__(self, tT, dT, tR, iT) -> None:
        self.transmissionTime = None
        self.diseaseTransmission = None
        self.transmissionRadius = None
        self.infectedTime = None


class Person:
    def __init__(self, iD: int,  s = 'S') -> None:
        self.iD = iD
        self.status = s
        self.eRData = '' # either dead or immune 
        self.rTime = 0
        self.iTime = 0
        self.pos = [random.randrange(WIDTH+1),random.randrange(HEIGHT+1)]


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


def create_population() -> list:
    population = []
    a = 0 
    for i in range(NUMB_PEOPLE):
        if a < NUMB_STARTING_INFECTED:
            population.append(Person(i+1, s='I'))
            a+=1
        else:
            population.append(Person(i+1))
    return population


def create_disease() -> Class:
    return Disease(1,0.1,2,3)


def main_loop(population, day):
    """
    Move 
    Run checks
    At the end plus one to infection time and check if no longer infected. 
    """
    day +=1
    movement(population)

    s_group = create_group(0, 'S', population)
    i_group = create_group(0 ,'I', population) 

    for i_person in i_group:
        i_person.iTime += 1

    for s_person in s_group:
        for i_person in i_group:
            if check_inside_radius(i_person.pos[0], i_person.pos[1], s_person.pos[0], s_person.pos[1]):
                debugging(0, [i_person, s_person]) 
                s_person.rTime += 1
                if s_person.rTime >= T_TIME and random.random() < P * DT:
                    s_person.status = 'I'
        
    for i_person in i_group:
        if i_person.iTime > INFECTION_TOTAL_TIME:
            i_person.status = 'R'
    
    population = movement(population)

    return day 


def movement(population):
    # random chance to move, random amount they can move 
    notR_group = create_group(1 ,'R', population)
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
    if random.random() < MOVE_PROB:
        for person in notR_group:
            # x direction 
            x,y = debugging(1, [0, person])
            x_amount = random.randint(1, MAX_MOVE_AMOUNT)
            check_movement(0, WIDTH, x_amount, person)
            # y direction  
            check_movement(1, HEIGHT, random.randint(1, MAX_MOVE_AMOUNT) - x_amount, person)
            debugging(1, [1, person, x, y])


def check_movement(type, direction, amount, person):
    if person.pos[type] + amount < direction:
        person.pos[type] += amount
    elif person.pos[type] - amount > 0:
        person.pos[type] -= amount


def create_group(type , st : str, population) -> list:
    if type == 0:
        return [person for person in population if person.status == st]
    else:
        return [person for person in population if person.status != st]


def check_inside_radius(x,y,c_x,c_y):  
    if ((x - c_x) * (x - c_x) + (y - c_y) * (y - c_y) <= T_RADIUS * T_RADIUS):
        return True 


def count_stats(population) -> list[str]:
    s,i,r = 0,0,0
    for person in population:
        if person.status == 'S':
            s +=1
        elif person.status == 'I':
            i +=1
        elif person.status == 'R':
            r +=1
    return s,i,r


def debugging(tag, args : list):
    # if not DEBUG:
    #     return 
    if tag == 0:
        print(f'''
            Radius - {T_RADIUS}
            Infected - {args[0].iD}
            Susceptible - {args[1].iD}
            ''')
    elif tag == 1:
        if args[0] == 0:
            return args[1].pos[0], args[1].pos[1]
        else: 
            print(f'''
            original pos - {args[2], args[3]}
            new pos - {args[1].pos[0], args[1].pos[1]}
            ''')
    elif tag == 3:
        for p in args[0]:
            print(p.display_stats())
    elif tag == 4:
        s,i,r = count_stats(args[0])
        print(f'''
        Susceptible - {s}
        Infected - {i}
        Removed - {r}
        ''')
        

log = logger.DiscontinousLog()
a = True 
day = 0
log.log('program start')
if __name__ == "__main__":
    population = create_population()
    log.log('population created')
    while a == True:
        print(f'width : {WIDTH}, height : {HEIGHT}')
        #debugging(3, [population])
        
        day = main_loop(population, day)
        debugging(4, [population])
       
        b = input('>')
        if b == 'd':
            a = False
        print('-----------')
        #debugging(3, [population])


log.localDump('TASDAWD2')




