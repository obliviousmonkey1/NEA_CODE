from mainHandler import *
from view import *
import miscFunctions
import threading

'''
controls all the handlers
'''

class Main:
    def __init__(self, mH, view) -> None:
        self.mainHandler = mH
        self.view = view
        self.mainHandler.register(self)
        self.view.register(self)
    

    def pauseSimulation(self):
        self.mainHandler.setSimulationHandlerRunning(False)


    def runSimulation(self):
        self.mainHandler.runSimulationHandler()

    
    def setUpSimulationData(self):
        self.mainHandler.createAndPopulateDatabase()


    # misc funciton calls 
    def checkRandom(self, value) -> bool:
        return miscFunctions.randomCheck(value)
    
    def readConfig(self):
        return miscFunctions.readConfig()
    
    def writeConfig(self, data):
        return miscFunctions.writeConfig(data)

if __name__ == "__main__":
    # debug 
    import os 
    try:
        os.remove('/Users/parzavel/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db')
    except:
        pass
    #
    mainHandler = Handler()
    ui = UI()
    c = Main(mainHandler, ui)
    #ui.entryPoint()
    c.setUpSimulationData()
    c.runSimulation()
