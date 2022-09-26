import SIR_MODEL as sim
import sqlite3

"""
SIR_MODEL which runs all the maps simulations these are threaded and controlled in this file so that all of the maps are kept in sync 
and stuff and the day is the same for all maps etc 

needs to access databases to be able to populate map and stuff 
so it will go through and put all the maps that are in the table into a list 
it will then populate the population using the id 
so get the pop from the pop id in the map 
get the people from checking if their pop id is equal to that one 

thread the maps 0
"""

class Main():
    def __init__(self) -> None:
        self.maps = self.getMaps()

    def getMaps(self):
        conn = sqlite3.connect('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db')
        c = conn.cursor()   
        c.execute('''
        SELECT *
        FROM Map
        ''')
        return c.fetchall()


conn = sqlite3.connect('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db')
c = conn.cursor()

getPeople = '''
SELECT *
FROM Person, Map, Population
WHERE Population.mapID = Map.id and Person.populationID = Population.id
'''

getPeople = '''
SELECT *
FROM Person, Map, Population
WHERE Map.ID = Map.populationID = Population.id and Person.populationID = Map.populationID and Person.populationID = 1
'''
for i in range(2):
    c.execute(f'''
    SELECT *
    FROM Person, Map, Population
    WHERE Map.ID = {i+1} and Map.populationID = Population.id and Person.populationID = Population.id 
    ''')
    people = c.fetchall()
    print(people)

a = Main()
print(a.maps)

# a = []
# for person in people:
#     a.append(sim.Person(person[0], person[3]))

# for i in a:
#     print(i.getStatus)