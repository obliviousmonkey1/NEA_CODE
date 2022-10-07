import os 
import json
import tkinter as tk
from tkinter import ttk

FILE_PATH_SETTINGS = '~/Documents/NEA/NEA_CODE/program/createTools/settings.json'

"""
main menu which is the general collumns then you have sub menus so if 2 diseases it will created d1 d2 in sub menu 
"""
class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.geometry("960x540")
        self.minsize(960,540)
        self.maxsize(960,540)
        self.title('Setup')
        self.type = None
   
        # initialize data
        self.settings = ("Select option",
                        "General",
                        "Disease",
                        "Population",
                        "Person",
                        "Map")

        # set up variable
        self.option_var = tk.StringVar(self)
    
    def register(self, controller):
        self._controller = controller

    def entryPoint(self):
        #creates widgets
        self.create_wigets()
        self.mainloop()

    def setUpSimulation(self):
        self._controller.setUpSimulationData()

    def create_wigets(self):
        # padding for widgets using the grid layout
        paddings = {'padx': 5, 'pady': 5}

        # label
        label = ttk.Label(self,  text='Select option to edit:')
        label.grid(column=0, row=0, sticky=tk.W, **paddings)

        # option menu
        option_menu = ttk.OptionMenu(
            self,
            self.option_var,
            self.settings[0],
            *self.settings,
            command=self.option_changed)

        option_menu.grid(column=1, row=0, sticky=tk.W, **paddings)

        # output label
        self.output_label = ttk.Label(self, foreground='red')
        self.output_label.grid(column=0, row=1, sticky=tk.W, **paddings)

        button = ttk.Button(self, text='Start Simulation', command=self.setUpSimulation)
        button.grid(column=1, row=100, sticky=tk.S, **paddings)
    
    def updateSettings(self) -> None:
        paddings = {'padx': 5, 'pady': 5}
        
        for value, key in enumerate(self.data[self.type]):
            if  self.e[value].get() == "random":
                self.data[self.type][key][1] = 1
                self.data[self.type][key][0] = self.e[value].get()
            else:
                self.data[self.type][key][1] = 0
                self.data[self.type][key][0] = self.e[value].get()

        with open(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/createTools/settings.json'),'w') as file:
            json.dump(self.data, file)
        
        self.output_label.destroy()
        self.output_label = ttk.Label(self, foreground='green',text='changes have been applied')
        self.output_label.grid(column=0, row=100, sticky=tk.W, **paddings)

    def verification(self):
        paddings = {'padx': 5, 'pady': 5}

        values = [i.get() for i in self.e] 
        try:
            i = 0
            # type verification
            for key in self.data[self.type]:
                r = 0
                if values[i] == "random":
                    r = 1
                elif not values[i]:
                    raise ValueError(f'Missing value in {key}')
                elif self.data[self.type][key][3] == "str":
                    if not isinstance(values[i], str):
                       raise ValueError(f'Incorrect type in {key}')
                elif self.data[self.type][key][3] == "float":
                    if not isinstance(float(values[i]), float) or (float(values[i]) < 0.0):
                        raise ValueError(f'Incorrect type or negative value in {key}')
                elif self.data[self.type][key][3] == "int":
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
            self.updateSettings()
        except ValueError as err:
            self.output_label.destroy()
            self.output_label = ttk.Label(self, foreground='red',text=err.args)
            self.output_label.grid(column=1, row=101, sticky=tk.W, **paddings)


    def displaySettings(self, *args):
        paddings = {'padx': 5, 'pady': 5}

        with open(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/createTools/settings.json'),'r') as file:
            self.data = json.load(file)

        r = 1
        self.e = []
        self.l = []
        for key, value in self.data[self.type].items():
            label = ttk.Label(self,  text=key)
            label.grid(column=0, row=r, sticky=tk.W,**paddings)
            self.l.append(label)
            entry = tk.Entry(self) 
            entry.grid(column=1, row=r, sticky=tk.S,**paddings)
            entry.insert(0, value[0])
            self.e.append(entry)
            label = ttk.Label(self,  text=f'Example : {value[2]}')
            label.grid(column=2, row=r, sticky=tk.W,**paddings)
            self.l.append(label)
            label = ttk.Label(self,  text=f'Type : {value[3]}')
            label.grid(column=3, row=r, sticky=tk.W,**paddings)
            self.l.append(label)
            r+=1

        self.button2 = ttk.Button(self, text='Commit', command=self.verification)
        self.button2.grid(column=1, row=r, sticky=tk.S, **paddings)


    def option_changed(self, *args):
        if self.type != None:
            for label in self.l:
                label.destroy()
            for entry in self.e:
                entry.destroy()
            self.output_label.destroy()
            self.button2.destroy()
            
        if self.option_var.get() == 'General':
            self.type = "general"
        elif self.option_var.get() == 'Disease':
            self.type = "disease"
        elif self.option_var.get() == 'Population':
            self.type = "populations"
        elif self.option_var.get() == 'Person':
            self.type = "people"
        elif self.option_var.get() == 'Map':
            self.type = "maps"
            
        self.displaySettings()



