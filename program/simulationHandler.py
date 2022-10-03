FILE_PATH_DB = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db'
FILE_PATH_DBH = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_LOG = '/Users/parzavel/Documents/NEA/NEA_CODE/program/inhouse tools'

import sys
sys.path.append(FILE_PATH_LOG)
sys.path.append(FILE_PATH_DBH)

import dbHandler as dbH
import logger 

import simulation as model
import sqlite3
import threading
import multiprocessing
import timeit
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
PEOPLE_NUMBER = 200
MAP_NUMBER = 4

class Main():
    def __init__(self) -> None:
        self.__dbQueryHandler = dbH.DBManager(FILE_PATH_DB)
        self.__maps = self.populateMapsFromDatabase()
        self.__running = True


    def populateMapsFromDatabase(self):
       return self.__dbQueryHandler.getMaps()


    def sim(self, map, threadID):
        sim = model.Simulation(map)
        sim.day(threadID)
        print(f'Thread {threadID}')
        

    # need to sort out multiprocessing
    def run(self): 
        while self.__running:
            self.startTime = timeit.default_timer()
            print(f'startTime: {self.startTime}')
            self.threads = []
            for index, map in enumerate(self.__maps):
                # self.sim(map, index)
                #  x = multiprocessing.Process(target=self.sim, args=(map,index))
                x = threading.Thread(target=self.sim, args=(map,index))
                self.threads.append(x)
                x.start()
            for index, thread in enumerate(self.threads):
                thread.join()
            print(f'endTime: {timeit.default_timer()}')
            print(f'time taken : {timeit.default_timer() - self.startTime}')
        
            # do stuff like update graph idk some other stuff
            input('> ')
            self.__maps = self.populateMapsFromDatabase()
                

    def setRunning(self, value: bool) -> None:
        self.__running = value


if __name__ == "__main__":
    Main()
