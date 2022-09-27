import sqlite3

FILE_PATH = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db'

"""
person and pop have one to many
pop to map has one to one
in order to be able to go through old data the db should be named after what the user decides to name the simulation 
"""

createPersonTable = '''
CREATE TABLE IF NOT EXISTS Person(
    id          INTEGER,
    status      TEXT,
    rTime       INTEGER,
    iTime       INTEGER,
    xPos        INTEGER,
    yPos        INTEGER,
    populationID    INTEGER,    
    FOREIGN KEY(populationID) REFERENCES Population(id),
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
    id          INTEGER,
    name        TEXT,
    width       INTEGER,
    height      INTEGER,
    day         INTEGER,
    populationID       INTEGER,
    FOREIGN KEY(populationID) REFERENCES Population(id),
    PRIMARY KEY(id)
);
'''
  
conn = sqlite3.connect(FILE_PATH)
c = conn.cursor()
c.execute(createPersonTable)
c.execute(createPopulationTable)
c.execute(createMapTable)
c.close()



