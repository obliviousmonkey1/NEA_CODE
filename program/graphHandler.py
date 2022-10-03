FILE_PATH = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_DB = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db'

import sys

sys.path.append(FILE_PATH)

from itertools import count 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import dbHandler as dbH


'''
need to make a class which holds reference to the map ids 
'''

class Main:
    def __init__(self) -> None:
        pass

dbQueryHandler = dbH.DBManager(FILE_PATH_DB)

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()

def animate(i):
    days = [1,2,3,4]
    # susceptible = np.sum(dbQueryHandler.getAllSusceptible(1),dtype=int)
    # infected = np.sum(dbQueryHandler.getAllInfected(1),dtype=int)
    # removed = np.sum(dbQueryHandler.getAllRemoved(1),dtype=int)

    susceptible = [70,70,70,66]
    infected = [1,1,1,4]
    removed = [0,0,0,1]


    plt.cla()
    plt.plot(days, susceptible, label='susceptible')
    plt.plot(days, infected, label='infected')
    plt.plot(days, removed, label='removed')
    plt.legend(loc='upper left')
    plt.tight_layout()


# interval is in milli seconds
# ani = FuncAnimation(plt.gcf(),animate, interval=1000)

# plt.tight_layout()
# plt.show()

# nDays = 1
# '''
# need to get the day as welll so it can be summed up and organised via day
# '''
# print(dbQueryHandler.getAllSusceptible(1))
# print(np.sum(dbQueryHandler.getAllSusceptible(1),dtype=int))
# print(np.sum(dbQueryHandler.getAllInfected(1),dtype=int))
# print(np.sum(dbQueryHandler.getAllRemoved(1),dtype=int))

# if __name__ == "__main__":
#     ani = FuncAnimation(plt.gcf(),animate, interval=1000)
#     plt.tight_layout()
#     plt.show()  
