from ast import Delete
from multiprocessing import Value
import os 
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image 
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.figure import Figure
import numpy as np

FILE_PATH_SETTINGS = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json'

"""
main menu which is the general collumns then you have sub menus so if 2 diseases it will created d1 d2 in sub menu 
"""
class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.parent = tk.Tk()
        self.controller = None
        self.type = "general"
        self.currentIndex = 0
        self.c = 0
        self.optionMenuIndex = 0
        self.settings = []
        self.e = []
        self.valueLabel = []
        self.l = []
        self.values = []
        self.currentGraphReference = 'allCities'
        self.initialize_user_interface()


    def initialize_user_interface(self):
        # self.parent.iconphoto(False, tk.PhotoImage(Image.open('/Users/parzavel/Documents/NEA/NEA_CODE/program/runTimeFiles/icon.png')))
        self.windowSizeChange('960','540')
        self.parent.title('Setup')
        self.title('Data')

    
    def register(self, controller):
        self._controller = controller
    
    # SIMULATION SETUP 
    '''
    need to make this call graph handler and have all of this done in the grpah handler
    '''
    def gCurrentData(self):
        # data = pd.read_csv(os.path.expanduser(f'~/Documents/NEA/NEA_CODE/program/runTimeFiles/simData/{self.currentGraphReference}data.csv'))
        return self._controller.gGraphData()
        # x = data['day']
        # y1 = data['Susceptible']
        # y2 = data['Infected']
        # y3 = data['Removed']
        # fig = Figure(figsize=(5, 4), dpi=100)
        # fig.add_subplot(111).plot(x,y1,y2,y3,scalex='Day',scaley='Population')
        # return fig 

    def gCurrentGraph(self):
        data = self.gCurrentData()
        self.canvas = FigureCanvasTkAgg(data, master=self.parent)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.gToolBarWindow()

        # data =self.gCurrentData()
        # self.canvas = FigureCanvasTkAgg(data, master=self.parent)  # A tk.DrawingArea.
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack(anchor=tk.CENTER , expand=0)
        
    def gCity(self, cName):
        # self.currentGraphReference = self.option_var.get()
        # if cName != 'allCities':
        #     self.currentDaySusceptibleStatsLabel['text'] = f'Susceptible : {self._controller.gCurrentDaySusceptibleData(int(cName[-1]))}'

        self.toolbar.destroy()
        self.currentGraphReference = cName
        self._controller.sGraphRef(cName)
        self.option_menu = cName
        self.canvas.get_tk_widget().destroy()
        self.currentGraphLabel['text'] = self.currentGraphReference
        self.gCurrentGraph()

    def graphButtons(self):
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'r') as file:
            self.data = json.load(file) 

        i = 0
        cityNames = []
        for i in range((len(self.data['maps']))):
            for key, value in self.data['maps'][i].items():
                if key == 'cityName':
                    cityNames.append(value[0])
            i+=1
        cityNames.reverse()

        # self.settings = []
        # self.settings.append('allCities')
        # for cityName in cityNames:
        #     self.settings.append(cityName)

        # self.option_var = tk.StringVar(self)
        # self.optionMenuIndex = 0
        # option_menu = ttk.OptionMenu(
        #         self,
        #         self.option_var,
        #         self.settings[self.optionMenuIndex],
        #         *self.settings,
        #         command=self.gCity())

        # option_menu.pack(anchor=tk.S, side=tk.RIGHT)

        button = ttk.Button(self.graphSelctorWindow, text='All Cities', command=lambda cName='allCities': self.gCity(cName))
        button.pack(anchor=tk.S, side=tk.LEFT)  
        for cityName in cityNames:
            button = ttk.Button(self.graphSelctorWindow, text=cityName, command=lambda cName=cityName: self.gCity(cName))
            button.pack(anchor=tk.S, side=tk.LEFT)
        
        button = ttk.Button(self, text='Step sim', command=self.rSim)
        button.pack(anchor=tk.S, side=tk.LEFT)


    def rSim(self):
        self._controller.runSimulation()

    def simulationWindow(self, value=0):
        if value == 1:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
            self.currentDayLabel.destroy()
            self.currentGraphLabel.destroy()
        self.parent.title('Simulation')

        self.currentDayLabel = ttk.Label(self, text=f'Current Day {(self._controller.getCurrentDay())}')
        self.currentDayLabel.pack(anchor=tk.NW, side=tk.LEFT) 

        self.currentGraphLabel = ttk.Label(self, text=f'Selected Graph {self.currentGraphReference}')
        self.currentGraphLabel.pack(anchor=tk.NW, side=tk.LEFT) 

        # self.currentDayStatsLabel = ttk.Label(self,text='Current day stats:')
        # self.currentDayStatsLabel.pack(anchor=tk.W, side=tk.LEFT) 

        # print(self.currentGraphReference)
        # if self.currentGraphReference != 'allCities':
        #     self.currentDaySusceptibleStatsLabel = ttk.Label(self,text=f'Susceptible : {self._controller.gCurrentDaySusceptibleData(int(self.currentGraphReference[-1]))}')
        #     self.currentDaySusceptibleStatsLabel.pack(anchor=tk.W, side=tk.LEFT) 
        #     self.currentDayInfectedStatsLabel = ttk.Label(self,text='Current day stats:')
        #     self.currentDayRemovedStatsLabel = ttk.Label(self,text='Current day stats:')


        self.gCurrentGraph()
        if value == 0:
            self.graphButtons()

        # run code 
        # self._controller.runSimulation()
  
    def gToolBarWindow(self):
        # self.toolBarWindow = tk.Tk()
        # self.toolBarWindow.title = 'Toolbar'
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.parent)
        self.toolbar.update()


    def loading(self):
        self.clearWidgets()
        self.windowSizeChange('960','540')
        self.parent.title('Loading')

        label = ttk.Label(self.parent, foreground='red', text='Failed to/taking time to Setting Up DataBase and other stuff')
        label.grid(column=1, row=1)
        self.parent.grid_rowconfigure(1, weight=1)
        self.parent.grid_columnconfigure(1, weight=1)

        self._controller.setUpSimulationData()
        print('compeleted')

        label.destroy()
        label = ttk.Label(self.parent, foreground='green', text='Setup complete')
        label.grid(column=1, row=1)
        label.destroy()
        # label.after(3000, lambda: label.destroy())    

        self.graphSelctorWindow = tk.Tk()
        self.graphSelctorWindow.title('Graph Selection')

        self._controller.sGraphRef(self.currentGraphReference)


        self.simulationWindow()

    # CONFIG SETUP
    def typeLoop(self):
        ty = 0
        for p in range(len(self.e)):
            self.values = [x.get() for x in self.e[p]] 
            if self.type != 'general':
                if ty == 0:
                    self.type = 'maps'
                elif ty == 1:
                    self.type = 'disease'
                elif ty == 2:
                    self.type = 'populations'
            self.verification()
            ty += 1

        self.updateSettings()

    def updateData(self,key,value) -> None:   
        self.data[self.type][self.currentIndex][key][0] = value
        
    def updateSettings(self):
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'w') as file:
            json.dump(self.data, file)

        self.complete_label = ttk.Label(self.parent, foreground='green',text='change/s have been applied')
        self.complete_label.grid(column=3, row=100, sticky=tk.S)
        self.complete_label.after(3000, lambda: self.complete_label.destroy() )

    def verification(self):
        paddings = {'padx': 5, 'pady': 5}    
        try:
            i = 0
            for key in self.data[self.type][self.currentIndex]:
                isValueRandom = 0
                if self.randomCheck(self.values[i]):
                    isValueRandom = 1
                elif not self.values[i]:
                    raise ValueError(f'Missing value in {key}')
                elif self.data[self.type][self.currentIndex][key][2] == "str":
                    if not isinstance(self.values[i], str):
                        raise ValueError(f'Incorrect type in {key}')
                elif self.data[self.type][self.currentIndex][key][2] == "float":
                    if not isinstance(float(self.values[i]), float) or (float(self.values[i]) < 0.0):
                        raise ValueError(f'Incorrect type or negative value in {key}')
                elif self.data[self.type][self.currentIndex][key][2] == "int":
                    if not isinstance(int(self.values[i]), int) or (int(self.values[i]) < 0.0):
                        raise ValueError(f'Incorrect type or negative value in {key}')
                elif self.data[self.type][self.currentIndex][key][2] == "bool":
                    if not isinstance(int(self.values[i]), int) or (int(self.values[i]) < 0.0):
                        raise ValueError(f'Incorrect type or negative value in {key}')
                    if int(self.values[i]) > 1 or int(self.values[i]) < 0:
                        raise ValueError(f'Incorrect type or negative value in {key}')


                # special variable verification
                if key != "infectionTimeBeforeQuarantine" and key != "travelTime" and isValueRandom == 0 and self.data[self.type][self.currentIndex][key][2] == "float":
                    if (float(self.values[i]) < 0.0 or float(self.values[i]) > 1.0):
                        raise ValueError(f'{key} float cannot be less than 0.0 or greater than 1.0')
                if self.type == 'general':
                    if key == 'numberOfMaps':
                        if isValueRandom == 1:
                            raise ValueError(f'{key} cannot be random')
                        elif float(self.values[i]) == 0:
                            raise ValueError(f'{key} cannot be 0')
                if self.type == 'maps':
                    if key == 'minNumberOfConnections' and isValueRandom == 0:
                        if(int(self.data['general'][0]['numberOfMaps'][0]) <= int(self.values[i])):
                            raise ValueError(f'{key} {self.data[self.type][self.currentIndex][key][1]}{int(self.data["general"][0]["numberOfMaps"][0])-1}')
             
                self.updateData(key, self.values[i])
                i+=1
        except ValueError as err:
            self.errorLabel = ttk.Label(self.parent, foreground='red',text=err.args)
            self.errorLabel.grid(column=1, row=101, sticky=tk.W, **paddings)
            self.errorLabel.after(6000, lambda: self.errorLabel.destroy() )
 
    def displaySettings(self):
        paddings = {'padx': 5, 'pady': 5}

        r = 1

        label = ttk.Label(self.parent,  text=f'{self.type.upper()} :')
        label.grid(column=self.c, row=0, sticky=tk.W,**paddings)

        if self.type in ['maps','disease','populations']:
            option_menu = ttk.OptionMenu(
                self.parent,
                self.option_var,
                self.settings[self.optionMenuIndex],
                *self.settings,
                command=self.option_changed)
            option_menu.grid(column=self.c+1, row=0, sticky=tk.W, **paddings)

        p = []
        for key, value in self.data[self.type][self.currentIndex].items():
            label = ttk.Label(self.parent,  text=key)
            label.grid(column=self.c, row=r, sticky=tk.W,**paddings)
            self.l.append(label)
        
            entry = tk.Entry(self.parent) 
            entry.grid(column=self.c+1, row=r, sticky=tk.S,**paddings)
            entry.insert(0, value[0])
            p.append(entry)
            label = ttk.Label(self.parent,  text=f'{value[1]}')
            label.grid(column=self.c+2, row=r, sticky=tk.W,**paddings)
            self.l.append(label)
         
            r+=1
        self.e.append(p)
        
        commit_button = ttk.Button(self.parent, text='Commit', command=self.typeLoop)
        commit_button.grid(column=self.c+1, row=99, sticky=tk.S)

    def randomCheck(self, value):
        if not value.lower() == 'random':
            return False
        return True

    def setUpTwo(self):
        self.openSettings()
        self.clearWidgets()
        types = ['maps','disease','populations']
        self.c = 0
        for type in types:
            self.type = type
            self.displaySettings()
            self.c += 3

        back_button = ttk.Button(self.parent, text='BACK', command=self.back)
        back_button.grid(column=0, row=100, sticky=tk.S)

        simulation_button = ttk.Button(self.parent, text='Start Simulation', command=self.loading)
        simulation_button.grid(column=self.c//2, row=100, sticky=tk.S)


    def setSettings(self):
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'r') as file:
            data = json.load(file)
        numberOfCities =  data['general'][self.currentIndex]['numberOfMaps'][0]
        data['maps'] = []
        data['disease'] = []
        data['populations'] = []
        for i in range(int(numberOfCities)):
            data['maps'].append({"cityName": [f"city{i+1}", "city1", "str"],
                                 "govermentActionReliabilty" : [0.3,"0.0<value<1.0","float"],
                                 "minNumberOfConnections": [1, "0<value<maps", "int"],
                                 "infectionTimeBeforeQuarantine": [3.0,"0.0<value<∞","float"],
                                 "socialDistanceTriggerInfectionCount": [10, "1<value<∞", "int"],
                                 "identifyAndIsolateTriggerInfectionCount": [10, "1<value<∞", "int"],
                                 "travelProhibitedTriggerInfectionCount" : [10, "1<value<∞", "int"],
                                 "travelTime": [2.0, '1.0<value<∞', 'float']
                                })
            data['disease'].append({"name": ["random", "COVID", "str"], 
                                    "transmissionTime": ["random", "0.0<value<1.0", "float"], 
                                    "contagion": ["random", 2, "int"], 
                                    "transmissionRadius": ["random", "1<value<4", "int"], 
                                    "infectedTime": ["random", "0.0<value<1.0", "float"],
                                    "incubationTime": ["random", "0.0<value<1.0", "float"],
                                    "mutationChance": ["random", "0.0<value<1.0", "float"],
                                    "numbBloodTypesSusceptible" : ["random",  "0<value<8", "int"], 
                                    "ageMostSusceptible" : ["random", "10<value<100", "int"],
                                    "pAsymptomaticOnInfection": ["random", "0.0<value<1.0", "float"],
                                    "canKill" : [0, "0,1","bool"]
                                })
            data['populations'].append({"populationSize": [100, "0<value<∞", "int"],
                                        "travelRate" : [0.5,"0.0<value<1.0","float"],
                                        "socialDistanceProb" : [0.5,"0.0<value<1.0","float"],
                                        "numbStartingInfected" : [2,"0<value<popSize","int"]
                                })
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'w') as file:
            json.dump(data, file)

        self.settings = []
        for x in data['maps']:
            self.settings.append(x['cityName'][0])
        self.option_var = tk.StringVar(self.parent)
        self.cleanUp()
        self.optionMenuIndex = 0
        self.windowSizeChange('1488','540')
        self.setUpTwo()

    def back(self):
        self.cleanUp()
        self.windowSizeChange('960','540')

        self.currentIndex = 0
        self.type = 'general'
        self.c = 0
        self.clearWidgets()
        self.setUpOne()

    def setUpOne(self):
        self.openSettings()
        # self.clear_widgets()
        self.displaySettings()
        nextButton = ttk.Button(self.parent, text='Next', command=self.setSettings)
        nextButton.grid(column=1, row=100, sticky=tk.S)

    def clearWidgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
    
    def option_changed(self, *args):
        self.optionMenuIndex = self.settings.index(self.option_var.get())
        self.currentIndex = self.settings.index(self.option_var.get())
        self.cleanUp()
        self.setUpTwo()

    def cleanUp(self):
        self.e = []
        self.l = []

    def windowSizeChange(self,width,height):
        self.parent.geometry(f"{width}x{height}")
        self.parent.resizable(False,False)

    def openSettings(self):
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'r') as file:
            self.data = json.load(file)


    def entry_point(self):
        self.setUpOne()


