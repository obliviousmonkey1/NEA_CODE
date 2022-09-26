import SIR_MODEL as model
import sqlite3
import threading

"""
SIR_MODEL which runs all the maps simulations these are threaded and controlled in this file so that all of the maps are kept in sync 
and stuff and the day is the same for all maps etc 

needs to access databases to be able to populate map and stuff 
so it will go through and put all the maps that are in the table into a list 
it will then populate the population using the id 
so get the pop from the pop id in the map 
get the people from checking if their pop id is equal to that one 

thread the maps 0
"""

class Main():
    def __init__(self) -> None:
        self.maps = self.getMaps()

    # call/use the dbHandler
    def getMaps(self):
        conn = sqlite3.connect('/Users/parzavel/Documents/NEA/NEA_CODE/program/database/population.db')
        c = conn.cursor()   
        c.execute('''
        SELECT *
        FROM Map
        ''')
        return c.fetchall()


    def sim(self,map):
        sim = model.Simulation(map)
        sim.countStatistics()
        

    def run(self):
        running = True 
        while running:
            self.threads = []
            for map in self.maps:
                x = threading.Thread(target=self.sim, args=(map,))
                self.threads.append(x)
                x.start()
            for index, thread in enumerate(self.threads):
                thread.join()
        
            # do stuff like update graph idk some other stuff
            input('> ')


a = Main()
print(a.run())
