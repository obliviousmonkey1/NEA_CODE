from random import randint
"""
data structre of the map ?????
needs to be used in cretepopulation.py
take information from the settings.json
"""
import os
import json
FILE_PATH_SETTINGS = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json'


class Main:
    def __init__(self, dbH, settings) -> None:
        self.__dbQueryHandler = dbH
        self.tag = 'maps'
        self.setUp(settings)


    def setUp(self, settings):
        for key, value in settings[self.tag].items():
            if value[1] == 1:
                if key == 'numberOfMaps':
                    self.__numberOfMaps = randint(1,6)
                    settings[self.tag][key][0] = self.__numberOfMaps
                elif key == 'minNumberOfConnections':
                    self.__minNumberOfConnections = randint(1, (self.__numberOfMaps // 2))
                    settings[self.tag][key][0] = self.__minNumberOfConnections
                elif key == 'cityNames':
                    self.__cityNames = []
                    for i in range(self.__numberOfMaps):
                        self.__cityNames.append(f'city{i+1}')
                    settings[self.tag][key][0] = ','.join(self.__cityNames)
            else:
                if key == 'numberOfMaps':
                    self.__numberOfMaps = int(value[0])
                elif key == 'minNumberOfConnections':
                    self.__minNumberOfConnections = int(value[0])
                elif key == 'cityNames':
                    self.__cityNames = value[0].split(',')
        
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'w') as file:
            json.dump(settings, file)
        
        
    def addOne(self, i):
        return i + 1 

    def factors(self, f, n, i):
        if i > n:
            return []
        else:
            if (n % i) == 0:
                return [i] + self.factors(f, n, f(i))
            else:
                return self.factors(f, n, f(i))


    def generateMapSize(self, populationSize):
        factors = self.factors(self.addOne, populationSize,1)
        width = factors[len(factors)//2]
        return width, populationSize//width


    def createMap(self, id: int, populationID: int, populationSize: int):
        width, height = self.generateMapSize(populationSize)
        self.__dbQueryHandler.createMap(id,self.__cityNames[id-1],width,height,0,populationID)
        
    
    def connections(self):
        pass

    def getNumberOfMaps(self) -> int:
        return self.__numberOfMaps
    

    def getCityNames(self) -> list[str]:
        return self.__cityNames


    