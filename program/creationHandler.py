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


    # Starts the database table seeding process 
    def seedDatabase(self):
        self.seedGeneralDB()
        self.seedBloodTypeTable()
        self.__populationCreationHandler.seedPopulationTable(0, True)
        for id in range(1, self.__numberOfMaps+1):
            self.__populationCreationHandler.seedPopulationTable(id)
        self.__mapCreationHandler.seedRelationshipTable()


    # Creates and seeds the CSV file for each population 
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


    # Populates the General table in the database with the values
    def seedGeneralDB(self):
        self.__dbQueryHandler.createGeneral(self.__generalMutationChance, self.__numberOfMaps, self.__timeRequiredBetweenTravels)

    
    # Organises the general section of the json file into lists 
    # if the value from the json is random then it randomly allocates a value 
    # based on the key of the json value 
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


    # Starts the process of the JSON file data being organised 
    # into its sections once that has been done it
    # starts the seeding of the database 
    def setUpData(self):
        data = self._mainHandler.getReadConfig()
        data = self.setUpGeneral(data)
        self.__diseaseCreationHandler = cD.DiseaseCreationHandler(self.__dbQueryHandler, data)
        self.__populationCreationHandler = cP.PopulationCreationHandler(self.__dbQueryHandler, data)
        self.__mapCreationHandler = cM.MapCreationHandler(self.__dbQueryHandler, data)

        self._mainHandler.setWriteConfig(data)
        self.__populationCreationHandler.register(self)

        self.seedDatabase()
        self.createStatsCSV()


    # Starts the seeding of the Map database
    def startMapSeed(self, id, populationID, popSize):
        self.__mapCreationHandler.seedMapTable(id, populationID, popSize)


    # Returns the disease ID for the current disease 
    def getDiseaseID(self, populationID, pawnID):
        return self.__diseaseCreationHandler.generateDiseaseID(populationID,pawnID,self.getMapHandlerName(populationID))


    

    # Populates the blood type table in the database with the values 
    def seedBloodTypeTable(self):
        id = 1
        for bloodType in ['O+','O-','A+','A-','B+','B-','AB+','AB-']:
            self.__dbQueryHandler.createBloodType(id, bloodType)
            id +=1
    

    # returns a the value of the map width for the currently
    # selected map 
    def getMapWidth(self) -> int:
        return self.__mapCreationHandler.getCityWidth()


    # returns a the value of the map height for the currently
    # selected map 
    def getMapHeight(self) -> int:
        return self.__mapCreationHandler.getCityHeight()


    # returns a the value of the city name for the currently
    # selected map 
    def getMapHandlerName(self, id) -> str:
        return self.__mapCreationHandler.getCityName(id)
    

    # returns a the values of the city names of the maps
    def getMapHandlerNames(self) -> str:
        return self.__mapCreationHandler.getCityNames()
    

    # returns a the value of the population size for the current
    # population
    def getPopulationSizes(self) -> int:
        return self.__populationCreationHandler.getPopulationSize()
    

    # returns a the value of the infected amounts for the currently
    # selected population
    def getInfectedAmounts(self) -> int:
        return  self.__populationCreationHandler.getInfectedAmount()


    # returns a the value of the probability of asymptomatic for the currently
    # selected disease
    def getDiseasePasympto(self, id) -> float:
        return self.__diseaseCreationHandler.getPasymptomaticOnInfection(id)



