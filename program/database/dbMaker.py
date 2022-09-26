"""
population db has two tables population and person  is one to many 
"""
import sqlite3


createTablePerson = '''
CREATE TABLE IF NOT EXISTS Person(
    id          INTEGER,
    firstname   TEXT,
    lastname    TEXT,
    status      TEXT,
    populationID    INTEGER,    
    FOREIGN KEY(populationID) REFERENCES Population(id),
    PRIMARY KEY(id)
);
'''

createTablePopulation = '''
CREATE TABLE IF NOT EXISTS Population(
    id          INTEGER,
    PRIMARY KEY(id)
);
'''

createTableMap = '''
CREATE TABLE IF NOT EXISTS Map(
    id          INTEGER,
    name        TEXT,
    width       INTEGER,
    height      INTEGER,
    populationID       INTEGER,
    FOREIGN KEY(populationID) REFERENCES Population(id),
    PRIMARY KEY(id)
);
'''

insert = '''
INSERT INTO Person VALUES
(?,?,?,?,?)
'''

insert1 = '''
INSERT INTO Population VALUES
(?,?)
'''

getAllPeople = '''
SELECT * 
FROM Person

'''

getPeopleById = '''
SELECT *
FROM Person
WHERE id = ?
'''

getPeople = '''
SELECT *
FROM Person
'''

getPopulation = '''
SELECT Person.firstname
FROM Person, Population
WHERE Population.id = Person.populationID
'''

#c = conn.cursor()
# c.execute(createPerson)
# c.execute(createPopulation)
# adds these to table
# c.execute(insert, (1,'Alice','A','S',1))
# c.execute(insert, (2,'Bob','B','I',2))
# c.execute(insert1, (1,1))
# c.execute(getAllPeople)
# owners = c.fetchall()
# print(owners)

# c.execute(getPeopleById, (2,))
# owenerById = c.fetchone()
# print(owenerById)

# c.execute(getPopulation)
# population = c.fetchall()
# print(population)


def createMap(mapValues, populationValues):
    conn = sqlite3.connect('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db')

    c = conn.cursor()

    insert = '''
    INSERT INTO Map VALUES
    (?,?,?,?,?)
    '''
    c.execute(insert, (mapValues[0], mapValues[1], mapValues[2], mapValues[3], mapValues[4]))
    createPopulation(populationValues)
    conn.commit()
    c.close()



def createPopulation(populationValues):
    conn = sqlite3.connect('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db')
    c = conn.cursor()

    insert = '''
    INSERT INTO Population VALUES
    (?,?)
    '''
    c.execute(insert, (populationValues[0],populationValues[1]))
    conn.commit()
    c.close()



def createPerson(personValues):
    conn = sqlite3.connect('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db')
    c = conn.cursor()
    insert = '''
    INSERT INTO Person VALUES
    (?,?,?,?,?)
    '''
    c.execute(insert, (personValues[0], personValues[1], personValues[2], personValues[3], personValues[4]))
    conn.commit()
    c.close()

conn = sqlite3.connect('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db')
c = conn.cursor()
c.execute(createTablePerson)
c.execute(createTablePopulation)
c.execute(createTableMap)
c.close()



