FILE_PATH = '~/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_DB = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'

import sys
import os 
sys.path.append(os.path.expanduser(FILE_PATH))

import pandas as pd
import matplotlib.pyplot as plt
import dbHandler as dbH
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

'''
need to make a class which holds reference to the map ids 
maybe have the data update every hour so graph updates per hour in real time while sim is running
'''

class GraphDataHandler:
    def __init__(self) -> None:
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))

    def getMapData(self, id, type):

        if id != 's':
            if type == 'S':
                return self.__dbQueryHandler.getPopulationSusceptible(id)[0]
            elif type == 'I':
                return self.__dbQueryHandler.getPopulationInfected(id)[0]
            elif type == 'R':
                return self.__dbQueryHandler.getPopulationRemoved(id)[0]
            elif type == 'dID':
                return [i[0] for i in self.__dbQueryHandler.getAllDiseaseIDsInAmap(id)]
            elif type == 'dData':
                return self.__dbQueryHandler.getAllDiseaseInfoFromID(id)
            elif type == 'QI':
                return len(self.__dbQueryHandler.getPopulationQuarintineInfected(id))
            elif type == 'QT':
                return len(self.__dbQueryHandler.getPopulationQuarintineTravelling(id))
            elif type == 'IB':
                return len(self.__dbQueryHandler.getInfectedIncubating(id))
            elif type == 'IF':
                return len(self.__dbQueryHandler.getInfectedInfectious(id))
            else:
                # print(self.__dbQueryHandler.getPopulationTravelling(id))
                return len(self.__dbQueryHandler.getPopulationTravelling(id))
        else:
            if type == 'S':
                susceptible = 0
                mapIDs = [i[0] for i in self.__dbQueryHandler.getAllMapIDs()]
                for mapID in mapIDs:
                    susceptible += self.__dbQueryHandler.getPopulationSusceptible(mapID)[0]
                return susceptible
            elif type == 'I':
                infected = 0
                mapIDs = [i[0] for i in self.__dbQueryHandler.getAllMapIDs()]
                for mapID in mapIDs:
                    infected += self.__dbQueryHandler.getPopulationInfected(mapID)[0]
                return infected
            elif type == 'R':
                removed = 0
                mapIDs = [i[0] for i in self.__dbQueryHandler.getAllMapIDs()]
                for mapID in mapIDs:
                    removed += self.__dbQueryHandler.getPopulationRemoved(mapID)[0]
                return removed
                

    def setNewGraphRef(self,graphReference):
        self._graphReference = graphReference

    def getData(self):
        data = pd.read_csv(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/simData/{self._graphReference}data.csv'))
        x = data['day']
        y1 = data['Susceptible']
        y2 = data['Infected']
        # y3 = data['Removed']
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).plot(x,y1,y2,scalex='Day',scaley='Population')

        return fig
  

