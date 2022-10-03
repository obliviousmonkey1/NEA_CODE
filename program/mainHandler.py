import graphHandler as gH
import simulationHandler as sH
import creationHandler as cH

'''
controls all the handlers
'''

class Handler:
    def __init__(self) -> None:
        self.__graphHandler = gH.Main()
        self.__simulationHandler = sH.Main()


    def setSimulationHandlerRunning(self, value: bool):
        self.__simulationHandler.__running.setRunning(value)


    def runSimulationHandler(self):
        running = True 
        while running:
            self.__simulationHandler.run()


    def createAndPopulateDatabase(self):
        self.__creationHandler = cH.Main()

   