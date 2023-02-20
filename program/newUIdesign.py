import os 
import json
import tkinter as tk
from tkinter import ttk
from PIL import Image 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

FILE_PATH_SETTINGS = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json'

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


    # initializes the user interface 
    def initialize_user_interface(self):
        self.windowSizeChange('960','540')
        self.parent.title('Setup')
        self.withdraw()

    
    def register(self, controller):
        self._controller = controller


    # gets the current graph from the graphHandler
    def gCurrentData(self):
        return self._controller.gGraphData()
    
    
    # uses the graph from the graphHandler and puts it on the UI 
    def gCurrentGraph(self):
        data = self.gCurrentData()
        self.canvas = FigureCanvasTkAgg(data, master=self.parent)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.gToolBarWindow()


    # sets up the simulation UI for the newley selected graph 
    # resets the data values populating the UI 
    def gCity(self, cName):
        self.diseaseInfo = self._controller.gPopulationData(cName[-1],"dID")
        self.diseaseMenuIndex = 0

        # destroy 
        self.toolbar.destroy()
        self.currentDaySusceptibleStatsLabel.destroy()
        self.currentDayInfectedStatsLabel.destroy()
        self.currentDayRemovedStatsLabel.destroy()
        self.currentDayTravellingStatsLabel.destroy()
        self.currentDayQuarantineInfected.destroy()
        self.currentDayQuarantineTravelling.destroy()
        self.currentDayIncubating.destroy()
        self.currentDayInfectious.destroy()

        self.currentGraphReference = cName
        self._controller.sGraphRef(cName)
        self.option_menu = cName
        self.canvas.get_tk_widget().destroy()
        self.gCurrentGraph()
        self.dataUpdate()
        self.updateDInfo()
        self.title(f'Selected Graph:{self.currentGraphReference} Day:{self._controller.getCurrentDay()[0]}')


    # adds buttons for each map to the UI which can be clicked
    # to show data on sed map and a graph 
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

        button = ttk.Button(self.graphSelctorWindow, text='All Cities', command=lambda cName='allCities': self.gCity(cName))
        button.pack(anchor=tk.S, side=tk.LEFT)  
        for cityName in cityNames:
            button = ttk.Button(self.graphSelctorWindow, text=cityName, command=lambda cName=cityName: self.gCity(cName))
            button.pack(anchor=tk.S, side=tk.LEFT)
        
        button = ttk.Button(self, text='Step sim', command=self.rSim)
        button.pack(anchor=tk.CENTER, side=tk.TOP)


    # runs the simulation and once complete updates the graph 
    def rSim(self):
        self._controller.runSimulation()
        self.update()


    # The UI loop for the simulation 
    def simulationWindow(self, value=0):
        if value == 1:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
            self.currentDaySusceptibleStatsLabel.destroy()
            self.currentDayInfectedStatsLabel.destroy()
            self.currentDayRemovedStatsLabel.destroy()
            self.currentDayTravellingStatsLabel.destroy()
            self.currentDayQuarantineInfected.destroy()
            self.currentDayQuarantineTravelling.destroy()
            self.currentDayIncubating.destroy()
            self.currentDayInfectious.destroy()


        self.gCurrentGraph()
        if value == 0:
            self.graphButtons()
            self.diseaseInfoSetup()

        
        self.title(f'Selected Graph:{self.currentGraphReference} Day:{self._controller.getCurrentDay()[0]}')
        self.dataUpdate()


    # sets up the UI widgets and initial data for disease information
    def diseaseInfoSetup(self):
        data = [None for _ in range(10)]
        id = None

        button = ttk.Button(self.diseaseDataWindow, text='Next disease', command=lambda change=1: self.updateDInfo(change))
        button.pack(anchor=tk.CENTER, side=tk.TOP)

        self.diseaseInfo = self._controller.gPopulationData(self.currentGraphReference[-1],"dID")

        if self.diseaseInfo:
            self.diseaseInfo = list(dict.fromkeys(self.diseaseInfo))
            data = self._controller.gPopulationData(self.diseaseInfo[self.diseaseMenuIndex],"dData")
            id = data[0]
            data = data[1:]

            self.diseaseTransmissionTimeLabel = ttk.Label(self.diseaseDataWindow,text=f'Transmission time: {round(data[1], 2)}')
            self.diseaseInfectedTimeLabel = ttk.Label(self.diseaseDataWindow,text=f'Infected time: {round(data[4], 2)}')
            self.diseaseIncubationTimeLabel = ttk.Label(self.diseaseDataWindow,text=f'Incubation time: {round(data[5], 2)}')
            self.diseasePasymptomaticOnInfectionLabel = ttk.Label(self.diseaseDataWindow,text=f'P asymptomatic on infection: {round(data[8], 2)}')
            self.diseaseVirulenceLabel = ttk.Label(self.diseaseDataWindow,text=f'Virulence: {round(data[9],2)}')
            self.diseaseMutationChanceLabel = ttk.Label(self.diseaseDataWindow,text=f'Mutation chance: {round(data[7])}')
        else:
            self.diseaseTransmissionTimeLabel = ttk.Label(self.diseaseDataWindow,text=f'Transmission time: {data[1]}')
            self.diseaseInfectedTimeLabel = ttk.Label(self.diseaseDataWindow,text=f'Infected time: {data[4]}')
            self.diseaseIncubationTimeLabel = ttk.Label(self.diseaseDataWindow,text=f'Incubation time: {data[5]}')
            self.diseasePasymptomaticOnInfectionLabel = ttk.Label(self.diseaseDataWindow,text=f'P asymptomatic on infection: {data[8]}')
            self.diseaseVirulenceLabel = ttk.Label(self.diseaseDataWindow,text=f'Virulence: {data[9]}')
            self.diseaseMutationChanceLabel = ttk.Label(self.diseaseDataWindow,text=f'Mutation chance: {data[7]}')

        
        self.diseaseIDlabel = ttk.Label(self.diseaseDataWindow,text=f'ID: {id}')
        self.diseaseNameLabel = ttk.Label(self.diseaseDataWindow,text=f'Name: {data[0]}')
        self.diseaseContagionLabel = ttk.Label(self.diseaseDataWindow,text=f'Contagion: {data[2]}')
        self.diseaseTransmissionRadiusLabel = ttk.Label(self.diseaseDataWindow,text=f'Transmission radius: {data[3]}')
        self.diseaseAgeMostSusceptibleLabel = ttk.Label(self.diseaseDataWindow,text=f'Age most susceptible: {data[6]}')

        self.diseaseIDlabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseaseNameLabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseaseTransmissionTimeLabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseaseContagionLabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseaseTransmissionRadiusLabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseaseInfectedTimeLabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseaseIncubationTimeLabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseaseAgeMostSusceptibleLabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseaseMutationChanceLabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseasePasymptomaticOnInfectionLabel.pack(anchor=tk.CENTER, side=tk.TOP)
        self.diseaseVirulenceLabel.pack(anchor=tk.CENTER, side=tk.TOP)

    
    # when a new disease is displayed refreshes the old data using this 
    def updateDInfo(self, change=0):
        data = [None for _ in range(10)]
        id = None
      
        if self.diseaseInfo:
            if self.diseaseMenuIndex + change >= len(self.diseaseInfo):
                self.diseaseMenuIndex = 0
            else:
                self.diseaseMenuIndex += change

            self.diseaseInfo = list(dict.fromkeys(self.diseaseInfo))
            data = self._controller.gPopulationData(self.diseaseInfo[self.diseaseMenuIndex],"dData")
            id = data[0]
            data = data[1:]
            self.diseaseTransmissionTimeLabel['text'] = f'Transmission time: {round(data[1], 2)}'
            self.diseaseInfectedTimeLabel['text'] = f'Infected time: {round(data[4], 2)}'
            self.diseaseIncubationTimeLabel['text'] = f'Incubation time: {round(data[5], 2)}'
            self.diseasePasymptomaticOnInfectionLabel['text'] = f'P asymptomatic on infection: {round(data[8], 2)}'
            self.diseaseVirulenceLabel['text'] = f'Virulence: {round(data[9],2)}'
            self.diseaseMutationChanceLabel['text'] = f'Mutation chance: {round(data[7],2)}'


        else:
            self.diseaseTransmissionTimeLabel['text'] = f'Transmission time: {data[1]}'
            self.diseaseInfectedTimeLabel['text'] = f'Infected time: {data[4]}'
            self.diseaseIncubationTimeLabel['text'] = f'Incubation time: {data[5]}'
            self.diseasePasymptomaticOnInfectionLabel['text'] = f'P asymptomatic on infection: {data[8]}'
            self.diseaseVirulenceLabel['text'] = f'Virulence: {data[9]}'
            self.diseaseMutationChanceLabel['text'] = f'Mutation chance: {data[7]}'

        self.diseaseIDlabel['text'] = f'ID: {id}'
        self.diseaseNameLabel['text'] = f'Name: {data[0]}'
        self.diseaseContagionLabel['text'] = f'Contagion: {data[2]}'
        self.diseaseTransmissionRadiusLabel['text'] = f'Transmission radius: {data[3]}'
        self.diseaseAgeMostSusceptibleLabel['text'] = f'Age most susceptible: {data[6]}'

    
    # updates and adds the data on the population to the UI 
    def dataUpdate(self):
        self.currentDaySusceptibleStatsLabel = ttk.Label(self.simulationDataWindow,text=f'Total susceptible : {self._controller.gPopulationData(self.currentGraphReference[-1],"S")}')
        self.currentDayInfectedStatsLabel = ttk.Label(self.simulationDataWindow,text=f'Total infected : {self._controller.gPopulationData(self.currentGraphReference[-1],"I")}')
        self.currentDayRemovedStatsLabel = ttk.Label(self.simulationDataWindow,text=f'Removed : {self._controller.gPopulationData(self.currentGraphReference[-1],"R")}')
        self.currentDayTravellingStatsLabel = ttk.Label(self.simulationDataWindow,text=f'Travelling : {self._controller.gPopulationData(self.currentGraphReference[-1],"T")}')

        self.currentDayQuarantineInfected  = ttk.Label(self.simulationDataWindow,text=f'Quarantine infected : {self._controller.gPopulationData(self.currentGraphReference[-1],"QI")}')
        self.currentDayQuarantineTravelling  = ttk.Label(self.simulationDataWindow,text=f'Quarantine travelling : {self._controller.gPopulationData(self.currentGraphReference[-1],"QT")}')

        self.currentDayIncubating = ttk.Label(self.simulationDataWindow,text=f'Infected incubating: {self._controller.gPopulationData(self.currentGraphReference[-1],"IB")}')
        self.currentDayInfectious = ttk.Label(self.simulationDataWindow,text=f'Infected infectious : {self._controller.gPopulationData(self.currentGraphReference[-1],"IF")}')

        self.currentDaySusceptibleStatsLabel.pack(anchor=tk.W, side=tk.TOP) 
        self.currentDayInfectedStatsLabel.pack(anchor=tk.W, side=tk.TOP)
        self.currentDayInfectious.pack(anchor=tk.W, side=tk.TOP)
        self.currentDayIncubating.pack(anchor=tk.W, side=tk.TOP)
        self.currentDayRemovedStatsLabel.pack(anchor=tk.W, side=tk.TOP)
        self.currentDayTravellingStatsLabel.pack(anchor=tk.W, side=tk.TOP)
        self.currentDayQuarantineInfected.pack(anchor=tk.W, side=tk.TOP) 
        self.currentDayQuarantineTravelling.pack(anchor=tk.W, side=tk.TOP)


    # adds a tool bar to the graph to allow it to be moved about and zoomed
    # in and out off 
    def gToolBarWindow(self):
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.parent)
        self.toolbar.update()

    
    # while the database is being set up this gets the UI ready to display the 
    # simulation UI and sets stuff up 
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

        self.graphSelctorWindow = tk.Tk()
        self.graphSelctorWindow.geometry("+800+622")
        self.graphSelctorWindow.title('Graph Selection')

        self.simulationDataWindow = tk.Tk()
        self.simulationDataWindow.title('SIR data')

        self.diseaseDataWindow = tk.Tk()
        self.diseaseDataWindow.title('Disease data')

        self.simulationDataWindow.geometry("216x160+65+171")
        self.simulationDataWindow.resizable(False,False)
        self.geometry("302x30+474+622")
        self.resizable(False,False)

        self.diseaseDataWindow.geometry("216x250+65+328")
        self.diseaseDataWindow.resizable(False,False)
       
        self.parent.geometry('+347+25')

        self._controller.sGraphRef(self.currentGraphReference)
        self.deiconify()

        self.diseaseMenuIndex = 0

        self.parent.title('Simulation')

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
            self.validation()
            ty += 1

        self.updateSettings()


    # adds the value given to by the key in the database
    def updateData(self,key,value) -> None:   
        self.data[self.type][self.currentIndex][key][0] = value
        
    
    # updates the json file with the changes made by the user 
    # and displays a message on the UI saying changes have been applied 
    def updateSettings(self):
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'w') as file:
            json.dump(self.data, file)

        self.complete_label = ttk.Label(self.parent, foreground='green',text='change/s have been applied')
        self.complete_label.grid(column=3, row=100, sticky=tk.S)
        self.complete_label.after(3000, lambda: self.complete_label.destroy() )


    # validation 
    # validates the data given by the user making sure its 
    # in the correct format for each entry 
    def validation(self):
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
                    if not isinstance(int(self.values[i]), int) or (int(self.values[i]) < 0):
                        raise ValueError(f'Incorrect type or negative value in {key}')
                elif self.data[self.type][self.currentIndex][key][2] == "bool":
                    if not isinstance(int(self.values[i]), int) or (int(self.values[i]) < 0):
                        raise ValueError(f'Incorrect type or negative value in {key}')
                    if int(self.values[i]) > 1 or int(self.values[i]) < 0:
                        raise ValueError(f'Incorrect type or negative value in {key}')

                # special variable validation
                if isValueRandom == 0 and self.data[self.type][self.currentIndex][key][2] == "float":
                    if '\u221e' not in self.data[self.type][self.currentIndex][key][1]:
                        if float(self.values[i]) <  float(self.data[self.type][self.currentIndex][key][1][0]) or float(self.values[i]) > float(self.data[self.type][self.currentIndex][key][1][-3]):
                            raise ValueError(f'{key} float cannot be less than 0.0 or greater than 1.0')
                if self.type == 'general':
                    if key == 'numberOfMaps':
                        if isValueRandom == 1:
                            raise ValueError(f'{key} cannot be random')
                        elif float(self.values[i]) == 0:
                            raise ValueError(f'{key} cannot be 0')
                
                if self.type == 'disease':
                    if key == 'transmissionRadius':
                        if isValueRandom != 1 and int(self.values[i]) > 4:
                            raise ValueError(f'{key} cannot be greater than 4')
                    if key == 'numbBloodTypesSusceptible':
                        if isValueRandom != 1 and int(self.values[i]) > 8:
                            raise ValueError(f'{key} cannot be greater than 8')
                    if key == 'ageMostSusceptible':
                        if isValueRandom != 1 and (int(self.values[i]) < 10 or int(self.values[i])> 100):
                            raise ValueError(f'{key} cannot be greater than 100 or less than 10')

                if self.type == 'populations':
                    if key == 'numbStartingInfected':
                        if isValueRandom != 1 and (int(self.data['populations'][self.currentIndex]['populationSize'][0]) < int(self.values[i])):
                            raise ValueError(f'{key} has to be less than population size')

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
 

    # displays all the settings from the json file for 
    # population, map and disease on the UI, allowing the 
    # current values to be edited and commited 
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


    # checks if the value supplied is equal to random
    def randomCheck(self, value):
        if not value.lower() == 'random':
            return False
        return True


    # loads the population, map and disease settings from the json 
    # setting up the UI to fit it 
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


    # sets up the json document with the correct number of entries for 
    # each section ; map, disease and populations
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
                                 "travelQuarintineTime": [2.0,"0.0<value<∞","float"],
                                 "socialDistanceTriggerInfectionCount": [10, "1<value<∞", "int"],
                                 "identifyAndIsolateTriggerInfectionCount": [10, "1<value<∞", "int"],
                                 "travelProhibitedTriggerInfectionCount" : [10, "1<value<∞", "int"],
                                 "travelTime": [2.0, '1.0<value<∞', 'float']
                                })
            data['disease'].append({"name": ["random", "COVID", "str"], 
                                    "transmissionTime": ["random", "0.0<value<∞", "float"], 
                                    "contagion": ["random", 2, "int"], 
                                    "transmissionRadius": ["random", "1<value<4", "int"], 
                                    "infectedTime": ["random", "0.0<value<∞", "float"],
                                    "incubationTime": ["random", "0.0<value<∞", "float"],
                                    "ageMostSusceptible" : ["random", "10<value<100", "int"],
                                    "mutationChance": ["random", "0.0<value<1.0", "float"],
                                    "numbBloodTypesSusceptible" : ["random",  "0<value<8", "int"], 
                                    "pAsymptomaticOnInfection": ["random", "0.0<value<1.0", "float"],
                                    "virulence" : [0.0, "0.0<value<1.0","float"]
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

    
    # allows the user to move back to the previous page 
    def back(self):
        self.cleanUp()
        self.windowSizeChange('960','540')

        self.currentIndex = 0
        self.type = 'general'
        self.c = 0
        self.clearWidgets()
        self.setUpOne()

    
    # displays the general json settings 
    def setUpOne(self):
        self.openSettings()
        self.displaySettings()
        nextButton = ttk.Button(self.parent, text='Next', command=self.setSettings)
        nextButton.grid(column=1, row=100, sticky=tk.S)


    # clears all widgets currently on the UI
    def clearWidgets(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
    

    # changes the current pointer to make sure that it matches with the new 
    # value selected in the drop down menu
    def option_changed(self, *args):
        self.optionMenuIndex = self.settings.index(self.option_var.get())
        self.currentIndex = self.settings.index(self.option_var.get())
        self.cleanUp()
        self.setUpTwo()


    # clears all entries and labels  
    def cleanUp(self):
        self.e = []
        self.l = []


    # takes in two values to change the size of the window
    def windowSizeChange(self,width,height):
        self.parent.geometry(f"{width}x{height}")
        self.parent.resizable(False,False)


    # loads the json file 
    def openSettings(self):
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'r') as file:
            self.data = json.load(file)

    
    # entry point into the UI
    def entry_point(self):
        self.setUpOne()


