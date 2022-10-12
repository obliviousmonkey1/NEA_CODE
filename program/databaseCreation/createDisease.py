from random import randint 
'''
files deals with the handerling of making disease and it mutations, so creating a disease using the user
input as well as random generation based on factors 
'''

class Main:
    def __init__(self, dbH, settings) -> None:
        self.__dbQueryHandler = dbH
        self.tag = 'disease'
        self.setUp(settings)


    # disease id should take into account the city that its in 
    def setUp(self, settings):
        randomVariables = []
        for key, value in settings[self.tag].items():
            if value[1] == 1:
                if key == "name":
                   pass

                # randomVariables.append([key, ])
            if key == 'name':
                self.__diseaseID = value[0]
            elif key == 'transmissionTime':
                self.__transmissionTime = value[0]
            elif key == 'contagion':
                self.__contagion = value[0]
            elif key == 'transmissionRadius':
                self.__transmissionRadius = value[0]
            elif key == 'infectedTime':
                self.__infectedTime = value[0]
            elif key == 'incubationTime':
                self.__incubationTime = value[0]
            elif key == 'mutation_chance':
                self.mutationChance = value[0]
          


    def run(self):
        pass


    def createDisease(self):
        self.__dbQueryHandler.createDisease(self.__diseaseID,self.__diseaseName,self.__transmissionTime,self.__contagion,self.__transmissionRadius, self.__infectedTime, self.__incubationTime)
    

    def getDiseaseID(self) -> str:
        return self.__diseaseID