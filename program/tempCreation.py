FILE_PATH_DB = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db'
FILE_PATH = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database'
import sys

sys.path.append(FILE_PATH)

import sqlite3
import names
import random

import dbMaker


"""
map gets generated first
population can use the map to get a home 
access a json document with settings for population 
use data form the web 
that can be used to affet results 
store that data in database 
read it and use it to affect results and stuff
population is stored in a database 
two tables one called people the other called families (might change ot relationships if i add friends and such)
age:
https://www.statista.com/statistics/270370/age-distribution-in-the-united-kingdom/
sex:
https://www.statista.com/statistics/281240/population-of-the-united-kingdom-uk-by-gender/
health:
https://www.health.org.uk/evidence-hub/health-inequalities/proportion-of-population-reporting-good-health-by-age-and-deprivation
https://www.blood.co.uk/why-give-blood/blood-types/
"""

class population:
    pass

class db:
    pass

class person:
    pass

WIDTH = 5
HEIGHT = 5

WIDTH2 = 10
HEIGHT2 = 10


WIDTH = 10
HEIGHT = 10

WIDTH2 = 10
HEIGHT2 = 10


conn = sqlite3.connect(FILE_PATH_DB)
c = conn.cursor()


insert = '''
INSERT INTO Disease VALUES
(?,?,?,?,?,?,?)
'''
c.execute(insert, ('1','Disease1', 2.0, 0.1, 2, 3.0, 0.0))


insert = '''
INSERT INTO Population VALUES
(?)
'''
c.execute(insert, (1,))
c.execute(insert, (2,))
c.execute(insert, (3,))
c.execute(insert, (4,))


insert = '''
INSERT INTO Map VALUES
(?,?,?,?,?,?)
'''
c.execute(insert, (1, 'City1', WIDTH, HEIGHT, 0, 1))
c.execute(insert, (2, 'City2', WIDTH2, HEIGHT2, 0, 2))
c.execute(insert, (3, 'City3', WIDTH2, HEIGHT2, 0, 3))
c.execute(insert, (4, 'City4', WIDTH2, HEIGHT2, 0, 4))


insert = '''
INSERT INTO Person VALUES
(?,?,?,?,?,?,?,?,?)
'''
NUMB_PEOPLE = 200
NUMB_STARTING_INFECTED = 1
a = 0 
id = 1
for i in range(NUMB_PEOPLE):
    if a < NUMB_STARTING_INFECTED:
        c.execute(insert, (id,'I',0.0,0.0,0.0,random.randrange(WIDTH),random.randrange(HEIGHT),'1',1))
        a+=1
    else:
        c.execute(insert, (id,'S',0.0,0.0,None,random.randrange(WIDTH),random.randrange(HEIGHT),None,1))
    id +=1

a = 0 
for i in range(NUMB_PEOPLE):
    if a < NUMB_STARTING_INFECTED:
        c.execute(insert, (id,'I',0.0,0.0,0.0,random.randrange(WIDTH2),random.randrange(HEIGHT2),'1',2))

        a+=1
    else:
        c.execute(insert, (id,'S',0.0,0.0,None,random.randrange(WIDTH2),random.randrange(HEIGHT2),None,2))
    id +=1

a = 0 
for i in range(NUMB_PEOPLE):
    if a < NUMB_STARTING_INFECTED:
        c.execute(insert, (id,'I',0.0,0.0,0.0,random.randrange(WIDTH2),random.randrange(HEIGHT2),'1',3))

        a+=1
    else:
        c.execute(insert, (id,'S',0.0,0.0,None,random.randrange(WIDTH2),random.randrange(HEIGHT2),None,3))
    id +=1

a = 0 
for i in range(NUMB_PEOPLE):
    if a < NUMB_STARTING_INFECTED:
        c.execute(insert, (id,'I',0.0,0.0,0.0,random.randrange(WIDTH2),random.randrange(HEIGHT2),'1',4))

        a+=1
    else:
        c.execute(insert, (id,'S',0.0,0.0,None,random.randrange(WIDTH2),random.randrange(HEIGHT2),None,4))
    id +=1

conn.commit()
c.close()