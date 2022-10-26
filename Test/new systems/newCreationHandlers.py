'''

'''
class MainCreationHandler:
   def __init__(self) -> None:
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))
        dbM.createDB()

    def seedDatabase(self):
        # for travel 
        seedPopulationTable(0)
        for id in range(int(general['numberOfMaps']):
            seedPopulationTable(id)
            seedMapTable(id)

    def run(self):
        with open(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json')) as f:
            data = json.load(f)
        self.__diseaseCreationHandler = cD.Main(self.__dbQueryHandler, data)
        self.__populationCreationHandler = cP.Main(self.__dbQueryHandler, data)
        self.__mapCreationHandler = cM.Main(self.__dbQueryHandler, data)

        self.__populationCreationHandler.register(self)
    
    # called from population creation while people are being made 
    def getMapWidthAndHeight(id):
        return self.mapHandler.getWidth(id), self.mapHandler.getHeight(id)
    
    # called from population creation while people are being made 
    def getDiseaseIdentifier(id):
        return self.diseaseHandler.getDiseaseId(id)

    # called from population creation while people are being made 
    def setDisease(infectedID, susceptibleID):
        "disease id is going to be made up off day + infected id + susceptibleID + map name +  disease name"
        seedDiseaseTable()

class PopulationHandler:
    def __init__(self, dbH, settings) -> None:
        self.__dbQueryHandler = dbH
        self._handler = None
        self.setUp(settings)

    def register(self, mainHandler):
        self._handler = mainHandler

