""""
data structre of the map ?????
needs to be used in cretepopulation.py
take information from the settings.json
"""
class Main:
    def __init__(self, dbH, settings) -> None:
        self.__dbQueryHandler = dbH
        self.setUp(settings)


    def setUp(self, settings):
        self.__numberOfMaps = settings['numberOfMaps']
        self.__cityNames = settings['cityNames'].split(',')


    def createMap(self, id: int, name: str, width: int, height: int, day: int, populationID: int):
        self.__dbQueryHandler.createMap(id,name,width,height,day,populationID)
    

    def getNumberOfMaps(self) -> int:
        return self.__numberOfMaps
    

    def getCityNames(self) -> list[str]:
        return self.__cityNames


    def connections(self):
        pass
