from random import randint 
'''
files deals with the handerling of making disease and it mutations, so creating a disease using the user
input as well as random generation based on factors 
'''

class Main:
    def __init__(self, dbH, settings) -> None:
        self.__dbQueryHandler = dbH
        self.setUp(settings)


    # disease id should take into account the city that its in 
    def setUp(self, settings):
        randomVariables = []
        for key, value in settings.items():
            if value[1] == 1:
                if key == "name":
                   pass

                # randomVariables.append([key, ])
            self.__diseaseID = settings["name"][0]
            self.__diseaseName = settings["name"][0]
            self.__transmissionTime = settings["transmissionTime"][0]
            self.__contagion = settings["contagion"][0]
            self.__transmissionRadius = settings["infectedTime"][0]
            self.__infectedTime = settings["incubationTime"][0]
            self.__incubationTime = settings["mutation_chance"][0]


    def run(self):
        pass


    def createDisease(self):
        self.__dbQueryHandler.createDisease(self.__diseaseID,self.__diseaseName,self.__transmissionTime,self.__contagion,self.__transmissionRadius, self.__infectedTime, self.__incubationTime)
    

    def getDiseaseID(self) -> str:
        return self.__diseaseID