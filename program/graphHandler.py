FILE_PATH = '~/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_DB = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/database.db'

import sys
import os 
sys.path.append(os.path.expanduser(FILE_PATH))

import pandas as pd
import dbHandler as dbH
from matplotlib.figure import Figure


class GraphDataHandler:
    def __init__(self) -> None:
        self.__dbQueryHandler = dbH.DBManager(os.path.expanduser(FILE_PATH_DB))


    # gets data from the database in order to populate entries in the GUI 
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
                

    # sets a new graph reference
    def setNewGraphRef(self,graphReference):
        self._graphReference = graphReference


    # gets data from the current graphReferences csv file
    # and uses matplotlib to use it to return a graph 
    def getData(self):
        data = pd.read_csv(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/simData/{self._graphReference}data.csv'))
        x = data['day']
        y1 = data['Susceptible']
        y2 = data['Infected']
        # y3 = data['Removed']
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).plot(x,y1,y2,scalex='Day',scaley='Population')

        return fig
  

