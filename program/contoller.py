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
    

    def pauseSimulation(self):
        self.mainHandler.setSimulationHandlerRunning(False)

    def run(self):
        self.mainHandler.runSimulationHandler()

    def runSimulation(self):
        self.mainHandler.runSimulationHandler()
        self.view.simulationWindow(1)


    # thread this simulation with two threads one that updates progress bar
    # the other one that doesn't
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
    def getCurrentDay(self) -> int:
        return self.mainHandler.gCurrentDay()

    def checkRandom(self, value) -> bool:
        return miscFunctions.randomCheck(value)
    
    def readConfig(self):
        return miscFunctions.readConfig()
    
    def writeConfig(self, data):
        return miscFunctions.writeConfig(data)

if __name__ == "__main__":
    # clean up 
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
    #
    mainHandler = Handler()
    ui = UI()
    c = Main(mainHandler, ui)
    ui.entry_point() 
    ui.parent.mainloop()

