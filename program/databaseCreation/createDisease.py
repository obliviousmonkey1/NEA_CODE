from random import randint, uniform, random, choice

class DiseaseCreationHandler:
    def __init__(self, dbH, data) -> None:
        self.__dbQueryHandler = dbH
        self.tag = 'disease'
        self.setUp(data)


    # Organises the disease section of the json file into lists 
    # if the value from the json is random then it randomly allocates a value 
    # based on the key of the json value 
    def setUp(self, data):
        self.__name = []
        self.__transmissionTime = []
        self.__contagion = []
        self.__transmissionRadius = []
        self.__infectedTime = []
        self.__incubationTime = []
        self.__mutationChance = []
        self.__numbBloodTypesSusceptible = []
        self.__ageMostSusceptible = []
        self.__pAsymptomaticOnInfection = []
        self.__virulence = []

        for a in range((len(data[self.tag]))):
            for key, value in data[self.tag][a].items():
                if self.checkRandom(value[0]):
                    if key == 'name':
                        self.__name.append(f'disease{a+1}')
                        data[self.tag][a][key][0] = self.__name[-1]
                    elif key == 'transmissionTime':
                        self.__transmissionTime.append(uniform(2.0,5.0))
                        data[self.tag][a][key][0] = self.__transmissionTime[-1]
                    elif key == 'contagion':
                        self.__contagion.append(randint(1,50))
                        data[self.tag][a][key][0] = self.__contagion[-1]
                    elif key == 'transmissionRadius':
                        self.__transmissionRadius.append(randint(1,4))
                        data[self.tag][a][key][0] = self.__transmissionRadius[-1]
                    elif key == 'infectedTime':
                        self.__infectedTime.append(uniform(2.0,5.0))
                        data[self.tag][a][key][0] = self.__infectedTime[-1]
                    elif key == 'incubationTime':
                        self.__incubationTime.append(random())
                        data[self.tag][a][key][0] = self.__incubationTime[-1]
                    elif key == 'mutationChance':
                        self.__mutationChance.append(uniform(0.0,0.3))
                        data[self.tag][a][key][0] = self.__mutationChance[-1]
                    elif key == 'numbBloodTypesSusceptible':
                        self.__numbBloodTypesSusceptible.append(randint(0,5))
                        data[self.tag][a][key][0] = self.__numbBloodTypesSusceptible[-1]
                    elif key == 'ageMostSusceptible':
                        self.__ageMostSusceptible.append(randint(10,100))
                        data[self.tag][a][key][0] = self.__ageMostSusceptible[-1]
                    elif key == 'pAsymptomaticOnInfection':
                        self.__pAsymptomaticOnInfection.append(random())
                        data[self.tag][a][key][0] = self.__pAsymptomaticOnInfection[-1]
                    elif key == 'virulence':
                        self.__virulence.append(random())
                        data[self.tag][a][key][0] = self.__virulence[-1]

                else:
                    if key == 'name':
                        self.__name.append(value[0])
                    elif key == 'transmissionTime':
                        self.__transmissionTime.append(float(value[0]))
                    elif key == 'contagion':
                        self.__contagion.append(int(value[0]))
                    elif key == 'transmissionRadius':
                        self.__transmissionRadius.append(int(value[0]))
                    elif key == 'infectedTime':
                        self.__infectedTime.append(float(value[0]))
                    elif key == 'incubationTime':
                        self.__incubationTime.append(float(value[0]))
                    elif key == 'mutationChance':
                        self.__mutationChance.append(float(value[0]))
                    elif key == 'numbBloodTypesSusceptible':
                        self.__numbBloodTypesSusceptible.append(int(value[0]))
                    elif key == 'ageMostSusceptible':
                        self.__ageMostSusceptible.append(int(value[0]))
                    elif key == 'pAsymptomaticOnInfection':
                        self.__pAsymptomaticOnInfection.append(float(value[0]))
                    elif key == 'virulence':
                        self.__virulence.append(float(value[0]))
            a+=1
           
        return data

    
    # Checks if the value in the json file is the word random
    def checkRandom(self, value):
        try:
            if not value.lower() == 'random':
                return False
            return True
        except:
            return False


    # Creates an ID to use in the database for the disease table
    def generateDiseaseID(self, populationID, pawnID, mapName):
        self.__diseaseID = f"{0}.{pawnID}.{pawnID}.{mapName}.{self.__name[populationID-1]}"
        self.seedDiseaseTable(populationID)
        return  self.__diseaseID


    # Populates the disease table in the database with the values 
    # of the current disease being added 
    def seedDiseaseTable(self, populationID):
        self.__dbQueryHandler.createDisease(self.__diseaseID, self.__name[(populationID-1)],
                                            self.__transmissionTime[(populationID-1)],self.__contagion[(populationID-1)],
                                            self.__transmissionRadius[(populationID-1)], self.__infectedTime[(populationID-1)], 
                                            self.__incubationTime[(populationID-1)], self.__ageMostSusceptible[(populationID-1)],
                                            self.__mutationChance[(populationID-1)], self.__pAsymptomaticOnInfection[(populationID-1)],
                                            self.__virulence[(populationID-1)]
                                            )
        self.seedBloodTypeRelationshipTable(populationID)


    # Randomly creates x ammount (a value specified at run time) 
    # of relationships between a bloodtypes and a disease 
    # this is then added into the blood type link relational table
    def seedBloodTypeRelationshipTable(self, populationID):
        bloodTypes = ['O+','O-','A+','A-','B+','B-','AB+','AB-']
        bloodTypesUsed = []
        for _ in range(self.__numbBloodTypesSusceptible[(populationID-1)]):
            bloodTypeAlreadyUsed = True 
            while bloodTypeAlreadyUsed:
                bloodType = choice(bloodTypes)
                if bloodType not in bloodTypesUsed:
                    bloodTypeAlreadyUsed = False
            self.__dbQueryHandler.createDiseaseBloodTypeLink(self.__diseaseID,(bloodTypes.index(bloodType)+1))
            bloodTypesUsed.append(bloodType)


    # returns a the value of propability of asymptomatic for the currently
    # selected disease 
    def getPasymptomaticOnInfection(self, id) -> float:
        return self.__pAsymptomaticOnInfection[id-1]