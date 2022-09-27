FILE_PATH_DB = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db'
FILE_PATH_LOG = '/Users/parzavel/Documents/NEA/NEA_CODE/program/inhouse tools'

import sys
sys.path.append(FILE_PATH_LOG)
sys.path.append(FILE_PATH_DB)

import dbHandler as dbH
import logger 

import simulation as model
import sqlite3
import threading
import random

"""
SIR_MODEL which runs all the maps simulations these are threaded and controlled in this file so that all of the maps are kept in sync 
and stuff and the day is the same for all maps etc 

needs to access databases to be able to populate map and stuff 
so it will go through and put all the maps that are in the table into a list 
it will then populate the population using the id 
so get the pop from the pop id in the map 
get the people from checking if their pop id is equal to that one 

thread the maps 0

load program, allow for editing of settings
then we load the dbMaker
then we load the createPopulation and createMap
then we run the main simulationHandler
"""
PEOPLE_NUMBER = 40
MAP_NUMBER = 2

class Main():
    def __init__(self) -> None:
        self.__dbQueryHandler = dbH.DBManager(FILE_PATH_DB)
        self.maps = self.populateMapsFromDatabase()
        self.run()


    def populateMapsFromDatabase(self):
       return self.__dbQueryHandler.getMaps()


    # Debugging (prevent having to delete the db over and over again)
    # really bad should just delete old population.db and then run dbMaker and createPop
    def resetPopulationTables(self): 
        for id in range(1, (PEOPLE_NUMBER+1)):
            if id == 1 or id == 21:
                self.__dbQueryHandler.updatePersonStatus(id, 'I')
            else:
                self.__dbQueryHandler.updatePersonStatus(id, 'S')
            self.__dbQueryHandler.updatePersonRtime(id, 0)
            self.__dbQueryHandler.updatePersonItime(id, 0)
            if id < 20:
                self.__dbQueryHandler.updatePersonXPos(id, random.randrange((self.__dbQueryHandler.getMapWidth(1))[0]))
                self.__dbQueryHandler.updatePersonYPos(id, random.randrange((self.__dbQueryHandler.getMapHeight(1))[0]))
            else:
                self.__dbQueryHandler.updatePersonXPos(id, random.randrange((self.__dbQueryHandler.getMapWidth(2))[0]))
                self.__dbQueryHandler.updatePersonYPos(id, random.randrange((self.__dbQueryHandler.getMapWidth(2))[0]))
        for id in range(1, (MAP_NUMBER+1)):
            self.__dbQueryHandler.updateMapDay(id, 0)


    def sim(self, map, threadID):
        sim = model.Simulation(map)
        sim.day()
        print(f'Thread {threadID}')
        sim.countStatistics()
        

    def run(self):
        running = True 
        while running:
            self.threads = []
            for index, map in enumerate(self.maps):
                x = threading.Thread(target=self.sim, args=(map,index))
                self.threads.append(x)
                x.start()
            for index, thread in enumerate(self.threads):
                thread.join()
        
            # do stuff like update graph idk some other stuff
            a = input('> ')
            if a == '1':
                self.resetPopulationTables()
                

if __name__ == "__main__":
    Main()
