import graphHandler as gH
import simulationHandler as sH
import creationHandler as cH

'''
controls all the handlers
'''

class Handler:
    def __init__(self) -> None:
        self.__graphHandler = gH.Main()
        self.__creationHandler = cH.Main()
        self.__simulationHandler = sH.Main()


    def setSimulationHandlerRunning(self, value: bool):
        self.__simulationHandler.__running.setRunning(value)


    def getUpdatedGraphs(self):
        pass


    def runSimulationHandler(self):
        self.__simulationHandler.run()


    def createAndPopulateDatabase(self):
        return self.__creationHandler.run()
   