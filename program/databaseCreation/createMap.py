from random import randint, random, uniform

import os
import json
FILE_PATH_SETTINGS = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json'


class MapCreationHandler:
    def __init__(self, dbH, data) -> None:
        self.__dbQueryHandler = dbH
        self.tag = 'maps'
        self.setUp(data)

    def setUp(self, data):

        self.__cityNames = []
        self.__govermentActionReliabilty = []
        self.__minNumberOfConnections = []
        self.__infectionTimeBeforeQuarantine = []
        self.__socialDistanceTriggerInfectionCount = []
        self.__identifyAndIsolateTriggerInfectionCount = []
        self.__travelTime = []
        self.__travelProhibitedTriggerInfectionCount = []

        for i in range((len(data[self.tag]))):
            for key, value in data[self.tag][i].items():
                if self.checkRandom(value[0]):
                    if key == 'cityName':
                        self.__cityNames.append(f'city{i+1}')
                        data[self.tag][i][key][0] = self.__cityNames[-1]
                    elif key == 'govermentActionReliabilty':
                        self.__govermentActionReliabilty.append(random())
                        data[self.tag][i][key][0] = self.__govermentActionReliabilty[-1]
                    elif key == 'minNumberOfConnections':
                        self.__minNumberOfConnections.append(randint(1, (int(data['general'][0]["numberOfMaps"][0]) // 2)))
                        data[self.tag][i][key][0] = self.__minNumberOfConnections[-1]
                    elif key == 'infectionTimeBeforeQuarantine':
                        self.__infectionTimeBeforeQuarantine.append(uniform(1.0,10.0))
                        data[self.tag][i][key][0] = self.__infectionTimeBeforeQuarantine[-1]
                    elif key == 'socialDistanceTriggerInfectionCount':
                        self.__socialDistanceTriggerInfectionCount.append(randint(10,20))
                        data[self.tag][i][key][0] = self.__socialDistanceTriggerInfectionCount[-1]
                    elif key == 'identifyAndIsolateTriggerInfectionCount':
                        self.__identifyAndIsolateTriggerInfectionCount.append(randint(10,20))
                        data[self.tag][i][key][0] = self.__identifyAndIsolateTriggerInfectionCount[-1]
                    elif key == 'travelTime':
                        self.__travelTime.append(uniform(1.0,3.0))
                        data[self.tag][i][key][0] = self.__travelTime[-1]
                    elif key == 'travelProhibitedTriggerInfectionCount':
                         self.__travelProhibitedTriggerInfectionCount(randint(5,10))
                else:
                    if key == 'cityName':
                        self.__cityNames.append(value[0])
                    elif key == 'govermentActionReliabilty':
                        self.__govermentActionReliabilty.append(float(value[0]))
                    elif key == 'minNumberOfConnections':
                        self.__minNumberOfConnections.append(int(value[0]))
                    elif key == 'infectionTimeBeforeQuarantine':
                        self.__infectionTimeBeforeQuarantine.append(float(value[0]))
                    elif key == 'socialDistanceTriggerInfectionCount':
                        self.__socialDistanceTriggerInfectionCount.append(int(value[0]))
                    elif key == 'identifyAndIsolateTriggerInfectionCount':
                        self.__identifyAndIsolateTriggerInfectionCount.append(int(value[0]))
                    elif key == 'travelTime':
                        self.__travelTime.append(value[0])
                    elif key == 'travelProhibitedTriggerInfectionCount':
                        self.__travelProhibitedTriggerInfectionCount.append(value[0])

            i+=1

        return data
        
    def checkRandom(self, value):
        try:
            if not value.lower() == 'random':
                return False
            return True
        except:
            return False

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


    def seedMapTable(self, id: int, populationID: int, populationSize: int):
        self.width, self.height = self.generateMapSize(populationSize)
        self.__dbQueryHandler.createMap(id,self.__cityNames[populationID-1],self.width,self.height,0,self.__govermentActionReliabilty[(populationID-1)],self.__identifyAndIsolateTriggerInfectionCount[(populationID-1)],self.__infectionTimeBeforeQuarantine[(populationID-1)],self.__socialDistanceTriggerInfectionCount[(populationID-1)],self.__travelProhibitedTriggerInfectionCount[populationID-1],self.__travelTime[(populationID-1)],0, populationID)
    
    def seedRelationshipTable(self):
        pass
    
    def connections(self):
        pass

    def getCityNames(self) -> list[str]:
        return self.__cityNames

    def getCityName(self,id) -> str:
        return self.__cityNames[id-1]
    
    def getCityWidth(self) -> int:
        return self.width
    
    def getCityHeight(self) -> int:
        return self.height


    
