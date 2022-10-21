# start stop system
'''
initialised as False
running is called true before program first run by UI
this will interact with the run_simulation_handler system  
start stop is going to be called by two buttons in the UI class 
'''
def start_stop(self, boolean) -> None:
    self.running = boolean

def run_simulation_handler(self):
    if self.running:
        # call simulation handler 
        pass