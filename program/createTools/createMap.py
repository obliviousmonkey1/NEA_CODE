""""
data structre of the map ?????
needs to be used in cretepopulation.py
"""
class Main:
    def __init__(self, dbH) -> None:
        self.__dbQueryHandler = dbH


    def createMap(self, id: int, name: str, width: int, height: int, day: int, populationID: int):
        self.__dbQueryHandler.createMap(id,name,width,height,day,populationID)