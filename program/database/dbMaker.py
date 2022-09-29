import sqlite3

FILE_PATH = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db'

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
createMapRelationshipsTable = ''''''

createTemporaryPopulationTable = ''''''

createTemporaryPersonTable = ''''''

# contain routines that people have one routine shared between many people 
createWeeklyRoutinesTable = ''''''
  
conn = sqlite3.connect(FILE_PATH)
c = conn.cursor()
c.execute(createPersonTable)
c.execute(createPopulationTable)
c.execute(createMapTable)
c.execute(createDiseaseTable)
c.execute(createStatisticsTable)
c.close()



