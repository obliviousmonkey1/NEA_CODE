import names
import random
import createMap

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

class Main:
    def __init__(self, dbH) -> None:
        self.__dbQueryHandler = dbH


class Population(Main):
    def __init__(self, dbH) -> None:
        super().__init__(dbH)
    
    def createPopulation(self, id: int, diseaseID: str, populationSize: int) -> None:
        self.__dbQueryHandler.createPopulation(id)
        Person(id, populationSize, diseaseID)
        

class Person(Main):
    def __init__(self, dbH, populatioID: int, diseaseID: str, populationSize: int) -> None:
        super().__init__(dbH)
        self.__populatioID = populatioID
        self.__diseaseID = diseaseID
        self.__populationSize = populationSize
        self.createPerson()
    

    # runs the person creation algorithm 
    def createPerson(self):
        pass


# NUMB_PEOPLE = 20
# NUMB_STARTING_INFECTED = 1
# a = 0 
# id = 1
# for i in range(NUMB_PEOPLE):
#     if a < NUMB_STARTING_INFECTED:
#         c.execute(insert, (id,'I',0.0,0.0,0.0,random.randrange(WIDTH),random.randrange(HEIGHT),'1',1))
#         a+=1
#     else:
#         c.execute(insert, (id,'S',0.0,0.0,None,random.randrange(WIDTH),random.randrange(HEIGHT),None,1))
#     id +=1
