FILE_PATH_DBH = '~/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_DB = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'
FILE_PATH_LOG = '~/Documents/NEA/NEA_CODE/program/inhouse tools'

import sys
import os
sys.path.append(os.path.expanduser(FILE_PATH_LOG))
sys.path.append(os.path.expanduser(FILE_PATH_DBH))

import dbHandler as dbH
import graphHandler as gH
import simulationHandler as sH
import creationHandler as cH


# controls all the handlers


class Handler:
    def __init__(self) -> None:
        self._controller = None
        self.__graphHandler = gH.GraphDataHandler()
        self.__creationHandler = cH.Main()
        self.__simulationHandler = sH.Main()
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))
        self.__creationHandler.register(self)
    

    def register(self, controller):
        self._controller = controller


    # runs the simulatoin handler
    def runSimulationHandler(self):
        self.__simulationHandler.run()


    # returns the current day of the simulation 
    def gCurrentDay(self):
        return self.__dbQueryHandler.getMapDay(1)


    # calls the setUpData method of the creationHandler class
    # to start the data setting up and seeding process
    def createAndPopulateDatabase(self):
        return self.__creationHandler.setUpData()


    # ui data
    # uses the graphHandler to get data on the populaiton for the UI
    def gFreshPopulationData(self, id, type):
        return self.__graphHandler.getMapData(id, type)


    # graph
    # uses the graphHandler to produce a graph and return it 
    def gNewGraphData(self):
        return self.__graphHandler.getData()


    # sets a new graph reference in the graph handler
    def sNewGraphRef(self, gR):
        self.__graphHandler.setNewGraphRef(gR)


    # gets the population suscpetible for a certain 
    # population from the database
    def getCurrentDaySusceptibleData(self, id):
        return self.__dbQueryHandler.getPopulationSusceptible(id)[0]


    # controller calls
    # checks if a the value passed is equal to the word random
    def checkRandom(self, value) -> bool:
        return self._controller.checkRandom(value)


    # returns the data from a json
    def getReadConfig(self):
        return self._controller.readConfig()


    # writes the data given to a json
    def setWriteConfig(self, data):
        return self._controller.writeConfig(data)

