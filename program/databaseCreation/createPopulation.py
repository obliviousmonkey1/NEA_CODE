from random import randint, random,randrange, choice


BLOOD_TYPES = ['O+','O-','A+','A-','B+','B-','AB+','AB-']


class PopulationCreationHandler:
    def __init__(self, dbH, data) -> None:
        self.__dbQueryHandler = dbH
        self._handler = None
        self.tag = 'populations'
        self.pawnID = 1
        self.setUp(data)
    
    def register(self, mainHandler):
        self._handler = mainHandler


    # Organises the population section of the json file into lists 
    # if the value from the json is random then it randomly allocates a value 
    # based on the key of the json value 
    def setUp(self, data):

        self.__populationSize = []
        self.__travelRate = []
        self.__socialDistanceProb = []
        self.__numbStartingInfected = []

        for i in range((len(data[self.tag]))):
            for key, value in data[self.tag][i].items():
                if self.checkRandom(value[0]):
                    if key == 'populationSize':
                        self.__populationSize.append(randint(80,600))
                        data[self.tag][i][key][0] = self.__populationSize[-1]
                    elif key == 'travelRate':
                        self.__travelRate.append(random())
                        data[self.tag][i][key][0] = self.__travelRate[-1]
                    elif key == 'socialDistanceProb':
                        self.__socialDistanceProb.append(random())
                        data[self.tag][i][key][0] = self.__socialDistanceProb[-1]
                    elif key == 'numbStartingInfected':
                        self.__numbStartingInfected.append(randint(1,self.__populationSize[-1]))
                        data[self.tag][i][key][0] = self.__numbStartingInfected[-1]
                else:
                    if key == 'populationSize':
                        self.__populationSize.append(int(value[0]))
                    elif key == 'travelRate':
                        self.__travelRate.append(float(value[0]))
                    elif key == 'socialDistanceProb':
                        self.__socialDistanceProb.append(float(value[0]))
                    elif key == 'numbStartingInfected':
                        self.__numbStartingInfected.append(int(value[0]))
            i+=1

        return data
        
    
    # Checks if the value in the json file is the word random
    def checkRandom(self, value):
        try:
            if not value.lower() == 'random':
                return False
            return True
        except:
            return False


    # Populates the Population table in the database with the values 
    # of the current map being added starts the seeding of the map
    # and population tied to that table if it has them
    def seedPopulationTable(self, populationID: int, indexZero=False) -> None:
        self.id = populationID
        self.__dbQueryHandler.createPopulation(self.id,0,0,0)
        if not indexZero:
            self.seedMap()
            self.seedPeopleTable()
    

    # Starts the process of the map seeding 
    def seedMap(self):
        self._handler.startMapSeed(self.id, self.id,self.__populationSize[(self.id-1)])


    # Starts the process of the population seeding, creating data for it 
    def seedPeopleTable(self):
        infected = 0 
        for _ in range(self.__populationSize[(self.id-1)]):
            pID = self.pawnID
            if infected < self.__numbStartingInfected[self.id-1]:
                status = 'I'
                infected += 1
                incubationTime = 0.0
                diseaseID = self._handler.getDiseaseID(self.id, pID)
                asymptomatic = self.setAsymptomatic()
            else:
                status = 'S'
                asymptomatic = None
                incubationTime = None
                diseaseID = None

            partialImmunity = None
            radiusTime = 0.0 
            infectedTime = 0.0
            xPos = randrange(self._handler.getMapWidth())
            yPos = randrange(self._handler.getMapHeight())
            travelling = 0
            travellingTime = 0.0
            destination = None
            bloodType = choice(BLOOD_TYPES)
            age = self.calcuateAge()
            health = 1-((age/100)**5)

            self.__dbQueryHandler.createPawn(pID,status,radiusTime,infectedTime,incubationTime,travellingTime,travelling,asymptomatic,partialImmunity,destination,bloodType,age,health,xPos,yPos,diseaseID,self.id)

            self.pawnID += 1


    # Generates an age for every pawn
    def calcuateAge(self) -> int:
        chance = random()
        if chance < 0.21:
            return randint(10,18)
        elif chance > 0.21 and chance < 0.5:
            return randint(18,39)
        elif chance > 0.5 and chance < 0.77:
            return randint(40,59)
        elif chance > 0.77:
            return randint(60,80)


    # Calculates whether an infected pawn is asymptomatic or not 
    def setAsymptomatic(self) -> int:
        if random() < self._handler.getDiseasePasympto(self.id):
            return 1 
        return 0


    # returns a the value of a population size for the currently
    # selected population 
    def getPopulationSize(self) -> int:
        return self.__populationSize
    

    # returns a the value of the infected amount for the currently
    # selected population 
    def getInfectedAmount(self) -> int:
        return self.__numbStartingInfected

