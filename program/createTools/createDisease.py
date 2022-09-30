'''
files deals with the handerling of making disease and it mutations, so creating a disease using the user
input as well as random generation based on factors 
'''
class Main:
    def __init__(self, dbH) -> None:
        self.__dbQueryHandler = dbH


    def createDisease(self, id: str, name: str, transmissionTime: float, contagion: float, transmissionRadius: int, infectedTime: float, incubationTime: float):
        self.__dbQueryHandler.createDisease(id,name,transmissionTime,contagion,transmissionRadius,infectedTime,incubationTime)