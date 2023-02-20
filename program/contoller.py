from mainHandler import *
from newUIdesign import *
import miscFunctions
import glob
import os 
import sys 

'''
controls all the handlers
'''

class Main:
    def __init__(self, mH, view) -> None:
        self.mainHandler = mH
        self.view = view
        self.mainHandler.register(self)
        self.view.register(self)
    

    # calls the main handler to start the simulation
    def runSimulation(self):
        self.mainHandler.runSimulationHandler()
        self.view.simulationWindow(1)


    # calls the create and populate database function from the mainHandler class
    def setUpSimulationData(self):
        self.mainHandler.createAndPopulateDatabase()


    # db 
    def gCurrentDaySusceptibleData(self, id):
        return self.mainHandler.getCurrentDaySusceptibleData(id)


    # ui data 
    def gPopulationData(self, id, type) -> int:
        return self.mainHandler.gFreshPopulationData(id, type)


    # graph
    def gGraphData(self):
        return self.mainHandler.gNewGraphData()


    def sGraphRef(self, gR):
        self.mainHandler.sNewGraphRef(gR)


    # misc funciton calls 
    # returns the current day in the simulation
    def getCurrentDay(self) -> int:
        return self.mainHandler.gCurrentDay()


    # checks if the value passed is equal to the word random
    def checkRandom(self, value) -> bool:
        return miscFunctions.randomCheck(value)


    # returns the data from a json file
    def readConfig(self):
        return miscFunctions.readConfig()


    # writes data to a json file 
    def writeConfig(self, data):
        return miscFunctions.writeConfig(data)


if __name__ == "__main__":
    # cleans up previous files and overides the base recursion depth limit to a deeper depth
    sys.setrecursionlimit(15000)
    os.chdir("/Users/parzavel/Documents/NEA/NEA_CODE/program/runTimeFiles/simData")
    extension = 'csv'
    allFilenames = [file for file in glob.glob('*.{}'.format(extension))]
    try:
        os.remove(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'))
        for file in allFilenames:
            os.remove(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/simData/{file}'))
    except:
        pass
    
    # initalises base classes and launches the ui
    mainHandler = Handler()
    ui = UI()
    c = Main(mainHandler, ui)
    ui.entry_point() 
    ui.parent.mainloop()

