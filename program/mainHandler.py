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

'''
controls all the handlers
'''

class Handler:
    def __init__(self) -> None:
        self._controller = None
        self.__graphHandler = gH.GraphDataHandler()
        self.__creationHandler = cH.Main()
        self.__simulationHandler = sH.Main()
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))

        # self.__graphHandler.register(self)
        self.__creationHandler.register(self)
        # self.__simulationHandler.register(self)
    

    def register(self, controller):
        self._controller = controller

    def setSimulationHandlerRunning(self, value: bool):
        self.__simulationHandler.__running.setRunning(value)

    def getUpdatedGraphs(self):
        pass

    def runSimulationHandler(self):
        self.__simulationHandler.run()

    def gCurrentDay(self):
        return self.__dbQueryHandler.getMapDay(1)

    def createAndPopulateDatabase(self):
        return self.__creationHandler.setUpData()

    # graph
    def gNewGraphData(self):
        return self.__graphHandler.getData()
    
    def sNewGraphRef(self, gR):
        self.__graphHandler.setNewGraphRef(gR)

    def getCurrentDaySusceptibleData(self, id):
        return self.__dbQueryHandler.getPopulationSusceptible(id)[0]
    # controller calls
    def checkRandom(self, value) -> bool:
        return self._controller.checkRandom(value)
    
    def getReadConfig(self):
        return self._controller.readConfig()
    
    def setWriteConfig(self, data):
        return self._controller.writeConfig(data)
   