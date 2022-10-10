from random import randint
"""
data structre of the map ?????
needs to be used in cretepopulation.py
take information from the settings.json
"""
class Main:
    def __init__(self, dbH, settings) -> None:
        self.__dbQueryHandler = dbH
        self.setUp(settings)


    def setUp(self, settings):
        for key, value in settings.items():
            if value[1] == 1:
                if key == 'numberOfMaps':
                    self.__numberOfMaps = randint(1,6)
                elif key == 'minNumberOfConnections':
                    print(self.__numberOfMaps)
                    self.__minNumberOfConnections = randint(1, (self.__numberOfMaps // 2))
                elif key == 'cityNames':
                    self.__cityNames = []
                    for i in range(self.__numberOfMaps):
                        self.__cityNames.append(f'city{i+1}')
            else:
                if key == 'numberOfMaps':
                    self.__numberOfMaps = int(value[0])
                elif key == 'minNumberOfConnections':
                    self.__minNumberOfConnections = int(value[0])
                elif key == 'cityNames':
                    self.__cityNames = value[0].split(',')
        
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


    
