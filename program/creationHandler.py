FILE_PATH_DB = '~/Documents/NEA/NEA_CODE/program/database/population.db'
FILE_PATH = '~/Documents/NEA/NEA_CODE/program/database'

import os 
import sys 
import json
sys.path.append(os.path.expanduser(FILE_PATH))
sys.path.append(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/createTools'))

import createMap as cM
import createPopulation as cP
import createDisease as cD
import dbHandler as dbH
import dbMaker as dbM

class Main:
    def __init__(self) -> None:
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))
        dbM
        print('hello')
        self.run()
    
    
    # create one map and one population at the same time and go through number of maps so if their were 3 maps
    # create population 1 and map 1 together then the next population 2 and map 2 etc ...
    def create(self):
        self.__diseaseCreationHandler.run()
        for i in range(1, self.__mapCreationHandler.getNumberOfMaps()+1):
            self.__populationCreationHandler.createPopulation(i , self.__diseaseCreationHandler.getDiseaseID())


    def run(self):
        with open(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/createTools/settings.json')) as f:
            data = json.load(f)
        self.__diseaseCreationHandler = cD.Main(self.__dbQueryHandler, data['disease'])
        self.__populationCreationHandler = cP.Main(self.__dbQueryHandler, data['populations'], data['people'])
        self.__mapCreationHandler = cM.Main(self.__dbQueryHandler, data['maps'])
        self.create()


