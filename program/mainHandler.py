import graphHandler as gH
import simulationHandler as sH
import creationHandler as cH
from view import *

'''
controls all the handlers
'''

class Controller:
    def __init__(self, gH, sH, cH, view) -> None:
        self.graphHandler = gH
        self.simulationHandler = sH
        self.creationHandler = cH
        self._view = view
        self._view.register(self)


if __name__ == "__main__":
    graphHandler = gH
    simulationHandler = sH
    creationHandler = cH
    ui = UI()
    c = Controller(graphHandler, simulationHandler, creationHandler, ui)
    ui.mainloop()