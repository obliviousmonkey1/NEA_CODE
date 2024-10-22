import sqlite3
import os

FILE_PATH = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'

# defines all the tables

createPawnTable = '''
CREATE TABLE IF NOT EXISTS Pawn(
    id              INTEGER,
    status          TEXT,
    rTime           FLOAT,
    iTime           FLOAT,
    ibTime          FLOAT,
    tTime           FLOAT,
    ntTime          FLOAT,
    travelling      INTEGER,
    asymptomatic    INTEGER,
    paritalImmunity FLOAT,
    sDestination    FLOAT,
    destination     INTEGER,
    bloodType       STRING,
    age             INTEGER,
    health          FLOAT,
    xPos            INTEGER,
    yPos            INTEGER,
    qTime           FLOAT,
    qInfected       INTEGER,
    qTravelling     INTEGER,
    arrivalCheck    INTEGER,   
    isInfectious    INTEGER,
    isIncubating    INTEGER,
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
    susceptible INTEGER,
    infected    INTEGER,
    removed     INTEGER,
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
    travelProhibitedTriggerInfectionCount   INTEGER,
    travelQuarintineTime                    FLOAT,
    travelTime                              FLOAT,
    travelProhibited                        INTEGER,
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
    mutationChance           FLOAT,
    pAsymptomaticOnInfection FLOAT,
    virulence                INTEGER,
    PRIMARY KEY(id)
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

createGeneralTable = '''
CREATE TABLE IF NOT EXISTS General(
    id                          INTEGER,
    generalMutationChance       FLOAT,
    numberOfMaps                INTEGER,
    timeRequiredBetweenTravels  FLOAT,
    PRIMARY KEY(id)
)
'''

# adds all the tables to a database 

def createDB():
    conn = sqlite3.connect(os.path.expanduser(FILE_PATH))
    c = conn.cursor()
    c.execute(createPawnTable)
    c.execute(createPopulationTable)
    c.execute(createMapTable)
    c.execute(createDiseaseTable)
    c.execute(createBloodTypeTable)
    c.execute(createDiseaseBloodTypeLinkTable)
    c.execute(createGeneralTable)
    c.close()



