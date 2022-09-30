FILE_PATH_DB = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db'
FILE_PATH = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database'

import sys 
sys.path.append(FILE_PATH)
sys.path.append('/Users/parzavel/Documents/NEA/NEA_CODE/program/createTools')

import createMap
import createPopulation
import createDisease
import dbHandler as dbH

class Main:
    def __init__(self) -> None:
        self.__dbQueryHandler = dbH.DBManager(FILE_PATH_DB)
        self.__createDiseaseHandler = createDisease.Main(self.__dbQueryHandler)
        self.__createPopulationHandler = createPopulation.Main(self.__dbQueryHandler)
        self.__createMapHandler = createMap.Main(self.__dbQueryHandler)
        self.run()
    
    
    def run(self):
        self.__createDiseaseHandler.createDisease('1','Disease1', 2.0, 0.1, 2, 3.0, 0.0)

if __name__ in "__main__": 
    Main()