import sqlite3
import os

FILE_PATH = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'


"""
person and pop have one to many
pop to map has one to one
in order to be able to go through old data the db should be named after what the user decides to name the simulation 
"""

createPersonTable = '''
CREATE TABLE IF NOT EXISTS Person(
    id              INTEGER,
    status          TEXT,
    rTime           FLOAT,
    iTime           FLOAT,
    ibTime          FLOAT,
    xPos            INTEGER,
    yPos            INTEGER,
    travelling      BOOLEAN,
    travellingTime  FLOAT,
    originalHome    INTEGER,
    diseaseID       INTEGER,
    populationID    INTEGER,    
    FOREIGN KEY(populationID) REFERENCES Population(id),
    FOREIGN KEY(diseaseID) REFERENCES Disease(id),
    PRIMARY KEY(id)
);
'''

createPopulationTable = '''
CREATE TABLE IF NOT EXISTS Population(
    id          INTEGER,
    PRIMARY KEY(id)
);
'''

createMapTable = '''
CREATE TABLE IF NOT EXISTS Map(
    id                 INTEGER,
    name               TEXT,
    width              INTEGER,
    height             INTEGER,
    day                INTEGER,
    populationID       INTEGER,
    FOREIGN KEY(populationID) REFERENCES Population(id),
    PRIMARY KEY(id)
);
'''

createDiseaseTable = '''
CREATE TABLE IF NOT EXISTS Disease(
    id                  STRING,
    name                TEXT,
    transmissionTime    FLOAT,
    contagion           FLOAT,
    transmissionRadius  INTEGER,
    infectedTime        FLOAT,
    incubationTime      FLOAT,
    PRIMARY KEY(id)
);
'''

createStatisticsTable = '''
CREATE TABLE IF NOT EXISTS Statistics(
    id          STRING,
    day         INTEGER,
    map         INTEGER, 
    susceptible INTEGER,
    infected    INTEGER,
    removed     INTEGER,
    PRIMARY KEY(id)  
);
'''

# mapRelationship or mapConnections
createMapRelationshipsTable = '''
CREATE TABLE IF NOT EXISTS MapRelationships(
    map1ID      ID,
    map2ID      ID,
    time        FLOAT, 
    drivable    BOOLEAN,
    flyable     BOOLEAN,
    FOREIGN KEY(map1ID) REFERENCES Map(id),
    FOREIGN KEY(map2ID) REFERENCES Map(id)
);
'''

createTemporaryPopulationTable = ''''''

createTemporaryPersonTable = ''''''

# contain routines that people have one routine shared between many people 
createWeeklyRoutinesTable = ''''''

def createDB():
    conn = sqlite3.connect(os.path.expanduser(FILE_PATH))
    c = conn.cursor()
    c.execute(createPersonTable)
    c.execute(createPopulationTable)
    c.execute(createMapTable)
    c.execute(createDiseaseTable)
    c.execute(createStatisticsTable)
    c.close()



