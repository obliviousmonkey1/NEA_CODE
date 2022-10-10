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
        self.mainHandler.createAndPopulateDatabase()
        return True 

if __name__ == "__main__":
    mainHandler = Handler()
    ui = UI()
    c = Main(mainHandler, ui)
    ui.entryPoint()
    # c.setUpSimulationData()
