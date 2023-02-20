FILE_PATH_DB = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'
FILE_PATH_DBH = '~/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_LOG = '~/Documents/NEA/NEA_CODE/program/inhouse tools'

import sys
import os 
import csv 
sys.path.append(os.path.expanduser(FILE_PATH_LOG))
sys.path.append(os.path.expanduser(FILE_PATH_DBH))

import dbHandler as dbH

import simulation as model
import sqlite3
import threading
import timeit
import random

"""
SIR_MODEL which runs all the maps simulations these are threaded and controlled in this file so that all of the maps are kept in sync 
and stuff and the day is the same for all maps etc 
"""
 

class Main():
    def __init__(self) -> None:
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))


    # returns all the maps in the map table in the database 
    def populateMapsFromDatabase(self):
       return self.__dbQueryHandler.getMaps()


    # calls the simulation file and starts a cycle for the map provided
    def sim(self, map, threadID):
        sim = model.Simulation(map)
        sim.day(threadID)
        print(f'Thread {threadID}')
        
    
    # returns the current day 
    def getDay(self) -> int:
        return self.__dbQueryHandler.getMapDay(1)


    # gets the maps from the database 
    # then splits the maps into seperate threads and calls the simulation code 
    # to start the simulation cycle
    def run(self): 
        self.__maps = self.populateMapsFromDatabase()
        self.startTime = timeit.default_timer()
        print(f'startTime: {self.startTime}')
        self.threads = []
        for index, map in enumerate(self.__maps):
            print(map)
            x = threading.Thread(target=self.sim, args=(map,index))
            self.threads.append(x)
            x.start()
        for index, thread in enumerate(self.threads):
            thread.join()
        print(f'endTime: {timeit.default_timer()}')
        print(f'time taken : {timeit.default_timer() - self.startTime}')
