from mainHandler import *
from view import *
import threading

'''
controls all the handlers
'''

class Main:
    def __init__(self, mH, view) -> None:
        self.mainHandler = mH
        self.view = view
        self.view.register(self)
    

    def pauseSimulation(self):
        self.mainHandler.setSimulationHandlerRunning(False)


    def runSimulation(self):
        self.mainHandler.runSimulationHandler()
    

    def setUpSimulationData(self):
        return self.mainHandler.createAndPopulateDatabase()


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
    ui.entry_point()
    # c.setUpSimulationData()
