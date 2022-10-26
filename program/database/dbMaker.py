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
    travellingTime  FLOAT,
    travelling      INTEGER,
    asymptomatic    INTEGER,
    paritalImmunity FLOAT,
    destination     INTEGER,
    bloodType       STRING,
    age             INTEGER,
    health          FLOAT,
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
    id                                      INTEGER,
    name                                    TEXT,
    width                                   INTEGER,
    height                                  INTEGER,
    day                                     INTEGER,
    govermentActionReliabilty               FLOAT,
    identifyAndIsolateTriggerInfectionCount INTEGER,
    infectionTimeBeforeQuarantine           FLOAT,
    socialDistanceTriggerInfectionCount     INTEGER,
    populationID                            INTEGER,
    FOREIGN KEY(populationID) REFERENCES Population(id),
    PRIMARY KEY(id)
);
'''

createDiseaseTable = '''
CREATE TABLE IF NOT EXISTS Disease(
    id                       STRING,
    name                     STRING,
    transmissionTime         FLOAT,
    contagion                FLOAT,
    transmissionRadius       INTEGER,
    infectedTime             FLOAT,
    incubationTime           FLOAT,
    ageMostSusceptible       INTEGER,
    canKill                  INTEGER,
    pAsymptomaticOnInfection FLOAT,
    danger                   FLOAT,
    PRIMARY KEY(id)
);
'''

# createStatisticsTable = '''
# CREATE TABLE IF NOT EXISTS Statistics(
#     id          STRING,
#     day         INTEGER,
#     map         INTEGER, 
#     susceptible INTEGER,
#     infected    INTEGER,
#     removed     INTEGER,
#     PRIMARY KEY(id)  
# );
# '''

# mapRelationship or mapConnections
createMapRelationshipsTable = '''
CREATE TABLE IF NOT EXISTS MapRelationships(
    map1ID      INTEGER,
    map2ID      INTEGER,
    time        FLOAT, 
    FOREIGN KEY(map1ID) REFERENCES Map(id),
    FOREIGN KEY(map2ID) REFERENCES Map(id)
);
'''
createBloodTypeTable = '''
CREATE TABLE IF NOT EXISTS BloodType(
    id          INTEGER,
    bloodType   STRING,
    PRIMARY KEY(id)
);
'''
createDiseaseBloodTypeLinkTable = '''
CREATE TABLE IF NOT EXISTS DiseaseBloodTypeLink(
    diseaseID        STRING,
    bloodTypeID      INTEGER,
    FOREIGN KEY(diseaseID) REFERENCES Disease(id),
    FOREIGN KEY(bloodTypeID) REFERENCES BloodType(id)
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
    c.execute(createMapRelationshipsTable)
    c.execute(createDiseaseTable)
    c.execute(createBloodTypeTable)
    c.execute(createDiseaseBloodTypeLinkTable)
    c.close()



