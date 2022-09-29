FILE_PATH = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database'
FILE_PATH_DB = '/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db'

import sys

sys.path.append(FILE_PATH)

import random
from itertools import count 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import dbHandler as dbH

dbQueryHandler = dbH.DBManager(FILE_PATH_DB)

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    susceptible = data['total_1']
    infected = data['total_2']
    removed = data['total_3']


    plt.cla()
    plt.plot(x, y1, label='Channel 1')
    plt.plot(x, y2, label='Channel 2')
    plt.legend(loc='upper left')
    plt.tight_layout()


# interval is in milli seconds
# ani = FuncAnimation(plt.gcf(),animate, interval=1000)

# plt.tight_layout()
# plt.show()

# print(dbQueryHandler.getAllSusceptible(1))
a = 0
for i in dbQueryHandler.getAllSusceptible(1):
    a += i[0]
print(a)
a = 0
for i in dbQueryHandler.getAllInfected(1):
    a += i[0]
print(a)
a = 0
for i in dbQueryHandler.getAllRemoved(1):
    a += i[0]
print(a)