import graphHandler as gH
import simulationHandler as sH
import creationHandler as cH

'''
controls all the handlers
'''

class Handler:
    def __init__(self) -> None:
        self._controller = None
        self.__graphHandler = gH.Main()
        self.__creationHandler = cH.Main()
        self.__simulationHandler = sH.Main()

        # self.__graphHandler.register(self)
        self.__creationHandler.register(self)
        # self.__simulationHandler.register(self)
    

    def register(self, controller):
        self._controller = controller

    def setSimulationHandlerRunning(self, value: bool):
        self.__simulationHandler.__running.setRunning(value)


    def getUpdatedGraphs(self):
        pass


    def runSimulationHandler(self):
        self.__simulationHandler.run()


    def createAndPopulateDatabase(self):
        return self.__creationHandler.setUpData()


    # controller calls
    def checkRandom(self, value) -> bool:
        return self._controller.checkRandom(value)
    
    def getReadConfig(self):
        return self._controller.readConfig()
    
    def setWriteConfig(self, data):
        return self._controller.writeConfig(data)
   