'''
files deals with the handerling of making disease and it mutations, so creating a disease using the user
input as well as random generation based on factors 
'''
import string


class Main:
    def __init__(self, dbH, settings) -> None:
        self.__dbQueryHandler = dbH
        self.setUp(settings)


    def setUp(self, settings):
        self.__diseaseID = settings["name"]


    def run(self):
        pass


    def createDisease(self, id: str, name: str, transmissionTime: float, contagion: float, transmissionRadius: int, infectedTime: float, incubationTime: float):
        self.__dbQueryHandler.createDisease(id,name,transmissionTime,contagion,transmissionRadius,infectedTime,incubationTime)
    

    def getDiseaseID(self) -> str:
        return self.__diseaseID