FILE_PATH_DB = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'
FILE_PATH = '~/Documents/NEA/NEA_CODE/program/database'

import csv
import os
import sys 
import json
sys.path.append(os.path.expanduser(FILE_PATH))
sys.path.append(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/databaseCreation'))

import createMap as cM
import createPopulation as cP
import createDisease as cD
import dbHandler as dbH
import dbMaker as dbM

from random import randint, random, uniform

class Main:
    def __init__(self) -> None:
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))
        self.tag = 'general'

        self._mainHandler = None
        dbM.createDB()
    
    def register(self, mH):
        self._mainHandler = mH

    def seedDatabase(self):
        self.seedGeneralDB()
        self.seedBloodTypeTable()
        self.__populationCreationHandler.seedPopulationTable(0, True)
        for id in range(1, self.__numberOfMaps+1):
            self.__populationCreationHandler.seedPopulationTable(id)
        self.__mapCreationHandler.seedRelationshipTable()

    def createStatsCSV(self):
        mapNames = self.getMapHandlerNames()
        populationSize = self.getPopulationSizes()
        infectedAmount = self.getInfectedAmounts()
        mapNames.append('allCities')
        for index in range(len(mapNames)):
            fieldnames = ["day", "Susceptible", "Infected", "Removed"]
            with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/simData/{mapNames[index]}data.csv'), 'w') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
            
            if mapNames[index] != 'allCities':
                with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/simData/{mapNames[index]}data.csv'), 'a') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
                    info={
                        "day" : 0,
                        "Susceptible" : populationSize[index]-infectedAmount[index],
                        "Infected" : infectedAmount[index],
                        "Removed" : 0
                    }
                    csv_writer.writerow(info)
            else:
                with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/simData/{mapNames[index]}data.csv'), 'a') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames) 
                    info={
                        "day" : 0,
                        "Susceptible" : 0,
                        "Infected" : 0,
                        "Removed" : 0
                    }
                    csv_writer.writerow(info)


    def seedGeneralDB(self):
        self.__dbQueryHandler.createGeneral(self.__generalMutationChance, self.__numberOfMaps, self.__timeRequiredBetweenTravels)

  
    def setUpGeneral(self, data):
        i = 0
       
        for key, value in data[self.tag][i].items():
            if self._mainHandler.checkRandom(value[0]):
                if key == 'generalMutationChance':
                    self.__generalMutationChance = uniform(0,0.3)
                    data[self.tag][i][key][0] = self.__generalMutationChance
                elif key == 'timeRequiredBetweenTravels':
                    self.__timeRequiredBetweenTravels = uniform(1.0, 4.0)
                    data[self.tag][i][key][0] = self.__timeRequiredBetweenTravels
            else:
                if key == 'generalMutationChance':
                    self.__generalMutationChance = float(value[0])
                elif key == 'numberOfMaps':
                    self.__numberOfMaps = int(value[0])
                elif key == 'timeRequiredBetweenTravels':
                    self.__timeRequiredBetweenTravels = float(value[0])
            i+=1

        return data 


    def setUpData(self):
        # pretty sure don't have to keep assigning data 
        data = self._mainHandler.getReadConfig()
        data = self.setUpGeneral(data)
        self.__diseaseCreationHandler = cD.DiseaseCreationHandler(self.__dbQueryHandler, data)
        self.__populationCreationHandler = cP.PopulationCreationHandler(self.__dbQueryHandler, data)
        self.__mapCreationHandler = cM.MapCreationHandler(self.__dbQueryHandler, data)

        self._mainHandler.setWriteConfig(data)
        self.__populationCreationHandler.register(self)

        self.seedDatabase()
        self.createStatsCSV()
        #return True 
    
    def startMapSeed(self, id, populationID, popSize):
        self.__mapCreationHandler.seedMapTable(id, populationID, popSize)

    def getDiseaseID(self, populationID, personID):
        return self.__diseaseCreationHandler.generateDiseaseID(populationID,personID,self.getMapHandlerName(populationID))

    def seedBloodTypeTable(self):
        id = 1
        for bloodType in ['O+','O-','A+','A-','B+','B-','AB+','AB-']:
            self.__dbQueryHandler.createBloodType(id, bloodType)
            id +=1
    
    def getMapWidth(self) -> int:
        return self.__mapCreationHandler.getCityWidth()

    def getMapHeight(self) -> int:
        return self.__mapCreationHandler.getCityHeight()

    def getMapHandlerName(self, id) -> str:
        return self.__mapCreationHandler.getCityName(id)
    
    def getMapHandlerNames(self) -> str:
        return self.__mapCreationHandler.getCityNames()
    
    def getPopulationSizes(self) -> int:
        return self.__populationCreationHandler.getPopulationSize()
    
    def getInfectedAmounts(self) -> int:
        return  self.__populationCreationHandler.getInfectedAmount()

    def getDiseasePasympto(self, id) -> float:
        return self.__diseaseCreationHandler.getPasymptomaticOnInfection(id)



