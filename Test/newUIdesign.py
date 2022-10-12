from ast import arg
import os 
import json
import tkinter as tk
from tkinter import ttk
import time



FILE_PATH_SETTINGS = '~/Documents/NEA/NEA_CODE/program/runTimeFiles/settings.json'

"""
main menu which is the general collumns then you have sub menus so if 2 diseases it will created d1 d2 in sub menu 
"""
class UI(tk.Tk):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.controller = None
        self.type = "general"
        self.currentIndex = 0
        self.optionMenuIndex = 0
        self.settings = []
        self.e = []
        self.l = []
        self.initialize_user_interface()
   
        # initialize data
        # self.settings = ("Select option",
        #                 "General",
        #                 "Disease",
        #                 "Population",
        #                 "Person",
        #                 "Map")

        # # set up variable
        # self.option_var = tk.StringVar(self)

    def initialize_user_interface(self):
        self.parent.geometry("960x540")
        self.parent.title('Setup')
        self.parent.minsize(960,540)
        self.parent.maxsize(960,540)
        self.entry_point()
    
    def register(self, controller):
        self._controller = controller
    
    def updateSettings(self) -> None:
        print('hi')
        paddings = {'padx': 5, 'pady': 5}
        
        ty = 0
        for p in range(len(self.e)):
            values = [x.get() for x in self.e[p]] 
            print(values)
            print(self.type)
            if self.type != 'general':
                if ty == 0:
                    self.type = 'maps'
                elif ty == 1:
                    self.type = 'disease'
                elif ty == 2:
                    self.type = 'populations'
                elif ty == 3:
                    self.type = 'people'

            i = 0 
            for value, key in enumerate(self.data[self.type][self.currentIndex]):
                self.data[self.type][self.currentIndex][key][0] = values[i]
                i += 1
            ty += 1

        with open(os.path.expanduser(FILE_PATH_SETTINGS),'w') as file:
            json.dump(self.data, file)
    
        if self.type != 'general':
            self.settings[self.settings.index(self.option_var.get())] = self.data['maps'][self.currentIndex]['cityName'][0]
        self.output_label = ttk.Label(self.parent, foreground='green',text='changes have been applied for all collumns')
        self.output_label.grid(column=3, row=100, sticky=tk.W, **paddings)

    def verification(self):
        paddings = {'padx': 5, 'pady': 5}    
        print(self.e)
        try:
            ty = 0
            # type verification
            for p in range(len(self.e)):
                values = [x.get() for x in self.e[p]] 
                print(values)
                if self.type != 'general':
                    if ty == 0:
                        self.type = 'maps'
                    elif ty == 1:
                        self.type = 'disease'
                    elif ty == 2:
                        self.type = 'populations'
                    elif ty == 3:
                        self.type = 'people'

                i = 0
                for key in self.data[self.type][self.currentIndex]:
                    r = 0
                    if values[i] == "random":
                        r = 1
                    elif not values[i]:
                        raise ValueError(f'Missing value in {key}')
                    elif self.data[self.type][self.currentIndex][key][3] == "str":
                        if not isinstance(values[i], str):
                            raise ValueError(f'Incorrect type in {key}')
                    elif self.data[self.type][self.currentIndex][key][3] == "float":
                        if not isinstance(float(values[i]), float) or (float(values[i]) < 0.0):
                            raise ValueError(f'Incorrect type or negative value in {key}')
                    elif self.data[self.type][self.currentIndex][key][3] == "int":
                        if not isinstance(int(values[i]), int) or (int(values[i]) < 0.0):
                            raise ValueError(f'Incorrect type or negative value in {key}')

                    # special variable verification
                    if self.type == 'maps':
                        if key == 'minNumberOfConnections' and r == 0:
                            if(int(values[0]) < int(values[i])):
                                raise ValueError(f'{key} cannot be larger than the number of cities')
                        elif key == 'cityNames' and r == 0:
                            if len(values[i].split(',')) != int(values[0]):
                                raise ValueError(f'{key} requires {values[0]} names since their are {values[0]} cities')
                        
                    i+=1
                ty +=1
            self.updateSettings()
        except ValueError as err:
            self.output_label.destroy()
            self.output_label = ttk.Label(self.parent, foreground='red',text=err.args)
            self.output_label.grid(column=1, row=101, sticky=tk.W, **paddings)


    def setUpSimulation(self):
        print('setUpSimulation')

    def displaySettings(self, c=0):
        paddings = {'padx': 5, 'pady': 5}

        with open(os.path.expanduser(FILE_PATH_SETTINGS),'r') as file:
            self.data = json.load(file)

        r = 1

        label = ttk.Label(self.parent,  text=f'{self.type.upper()} :')
        label.grid(column=c, row=0, sticky=tk.W,**paddings)

        if self.type in ['maps','disease','populations','people']:
            option_menu = ttk.OptionMenu(
                self.parent,
                self.option_var,
                self.settings[self.optionMenuIndex],
                *self.settings,
                command=self.option_changed)
            option_menu.grid(column=c+1, row=0, sticky=tk.W, **paddings)
        p = []
        for key, value in self.data[self.type][self.currentIndex].items():
            label = ttk.Label(self.parent,  text=key)
            label.grid(column=c, row=r, sticky=tk.W,**paddings)
            self.l.append(label)
            entry = tk.Entry(self.parent) 
            entry.grid(column=c+1, row=r, sticky=tk.S,**paddings)
            entry.insert(0, value[0])
            p.append(entry)
            # label = ttk.Label(self.parent,  text=f'Example : {value[2]}')
            # label.grid(column=c+2, row=r, sticky=tk.W,**paddings)
            # self.l.append(label)
            # label = ttk.Label(self.parent,  text=f'Type : {value[3]}')
            # label.grid(column=c+3, row=r, sticky=tk.W,**paddings)
            # self.l.append(label)
            r+=1
        self.e.append(p)
        
        commit_button = ttk.Button(self.parent, text='Commit', command=self.verification)
        commit_button.grid(column=c+1, row=r, sticky=tk.S, **paddings)

    def setUpTwo(self):
        self.clear_widgets()
        types = ['maps','disease','populations','people']
        c = 0
        for type in types:
            self.type = type
            self.displaySettings(c)
            c += 2

        simulation_button = ttk.Button(self.parent, text='BACK', command=self.setUpOne)
        simulation_button.grid(column=0, row=100, sticky=tk.S)

        simulation_button = ttk.Button(self.parent, text='Start Simulation', command=self.setUpSimulation)
        simulation_button.grid(column=c//2, row=100, sticky=tk.S)


    def setSettings(self):
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'r') as file:
            data = json.load(file)
        numberOfCities =  data['general'][self.currentIndex]['numberOfMaps'][0]
        data['maps'] = []
        data['disease'] = []
        data['populations'] = []
        data['people'] = []
        for i in range(int(numberOfCities)):
            data['maps'].append({"minNumberOfConnections": [1, 1, 2, "int"], "cityName": [f"city{i+1}", 1, "city1", "str"]})
            data['disease'].append({"name": ["random", 1, "bob", "str"], "transmissionTime": ["random", 1, 0.1, "float"], "contagion": ["random", 1, 2, "int"], "transmissionRadius": ["random", 1, 2, "int"], "infectedTime": ["random", 1, 0.2, "float"], "incubationTime": ["random", 1, 0.2, "float"], "mutation_chance": ["random", 1, 0.2, "float"]})
            data['populations'].append({"populationSize": [100, 0, 100, "int"]})
            data['people'].append({"dbREF": ["random", 1, "h", "str"]})
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'w') as file:
            json.dump(data, file)

        self.settings = []
        for x in data['maps']:
            self.settings.append(x['cityName'][0])
        self.option_var = tk.StringVar(self.parent)
        self.cleanUp()
        self.optionMenuIndex = 0
        self.setUpTwo()


    def setUpOne(self):
        self.cleanUp()
        self.currentIndex = 0
        self.type = 'general'
        self.clear_widgets()
        self.displaySettings()
        nextButton = ttk.Button(self.parent, text='Next', command=self.setSettings)
        nextButton.grid(column=1, row=100, sticky=tk.S)

    def clear_widgets(self):
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

    def entry_point(self):
        self.setUpOne()


if __name__ == '__main__':
   root = tk.Tk()
   run = UI(root)
   root.mainloop()
