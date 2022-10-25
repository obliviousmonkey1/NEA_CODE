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
        self.c = 0
        self.optionMenuIndex = 0
        self.settings = []
        self.e = []
        self.valueLabel = []
        self.l = []
        self.values = []
        self.initialize_user_interface()


    def initialize_user_interface(self):
        self.parent.geometry("960x540")
        self.parent.title('Setup')
        self.parent.resizable(False,False)
        self.entry_point()
    
    def register(self, controller):
        self._controller = controller
    
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
                elif ty == 3:
                    self.type = 'people'
            self.verification()
            ty += 1

        self.updateSettings()

    def updateData(self,key,value) -> None:   
        self.data[self.type][self.currentIndex][key][0] = value
        
       
    def updateSettings(self):
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'w') as file:
            json.dump(self.data, file)

        # if self.type != 'general':
        #     self.settings[self.settings.index(self.option_var.get())] = self.data['maps'][self.currentIndex]['cityName'][0]
        self.complete_label = ttk.Label(self.parent, foreground='green',text='changes have been applied')
        self.complete_label.grid(column=3, row=100, sticky=tk.S)
        self.complete_label.after(3000, lambda: self.complete_label.destroy() )


    def verification(self):
        paddings = {'padx': 5, 'pady': 5}    
        try:
            
            i = 0
            for key in self.data[self.type][self.currentIndex]:
                r = 0
                if self.values[i] == "random":
                    r = 1
                elif not self.values[i]:
                    raise ValueError(f'Missing value in {key}')
                elif self.data[self.type][self.currentIndex][key][3] == "str":
                    if not isinstance(self.values[i], str):
                        raise ValueError(f'Incorrect type in {key}')
                elif self.data[self.type][self.currentIndex][key][3] == "float":
                    if not isinstance(float(self.values[i]), float) or (float(self.values[i]) < 0.0):
                        raise ValueError(f'Incorrect type or negative value in {key}')
                elif self.data[self.type][self.currentIndex][key][3] == "int":
                    if not isinstance(int(self.values[i]), int) or (int(self.values[i]) < 0.0):
                        raise ValueError(f'Incorrect type or negative value in {key}')

                # special variable verification
                if self.type == 'general':
                    if key == 'numberOfMaps':
                        if r == 1:
                            raise ValueError(f'{key} cannot be random')
                if self.type == 'maps':
                    if key == 'minNumberOfConnections' and r == 0:
                        if(int(self.values[0]) < int(self.values[i])):
                            raise ValueError(f'{key} cannot be larger than the number of cities')
                    elif key == 'cityNames' and r == 0:
                        if len(self.values[i].split(',')) != int(self.values[0]):
                            raise ValueError(f'{key} requires {self.values[0]} names since their are {self.values[0]} cities')
             
                self.updateData(key, self.values[i])
                i+=1
        except ValueError as err:
            self.errorLabel = ttk.Label(self.parent, foreground='red',text=err.args)
            self.errorLabel.grid(column=1, row=101, sticky=tk.W, **paddings)
            self.errorLabel.after(3000, lambda: self.errorLabel.destroy() )


    def setUpSimulation(self):
        print('setUpSimulation')

    def openSettings(self):
        with open(os.path.expanduser(FILE_PATH_SETTINGS),'r') as file:
            self.data = json.load(file)

    def displaySettings(self):
        paddings = {'padx': 5, 'pady': 5}

        r = 1

        label = ttk.Label(self.parent,  text=f'{self.type.upper()} :')
        label.grid(column=self.c, row=0, sticky=tk.W,**paddings)

        if self.type in ['maps','disease','populations','people']:
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
            if value[3] == 'float' and self.randomCheck(value[0]):
                slider = ttk.Scale(self.parent, from_=0,to=1,orient='horizontal',value= value[0])
                slider.grid(column=self.c+1, row=r, sticky=tk.S,**paddings)
                self.valueLabel = ttk.Label(self.parent, text=slider.get())
                self.valueLabel.grid(column=self.c+2, row=r, sticky=tk.S,**paddings)
                p.append(slider)
                
            else:
                entry = tk.Entry(self.parent) 
                entry.grid(column=self.c+1, row=r, sticky=tk.S,**paddings)
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
        
        commit_button = ttk.Button(self.parent, text='Commit', command=self.typeLoop)
        commit_button.grid(column=self.c+1, row=99, sticky=tk.S)

    def randomCheck(self, value):
        if not value.lower == 'random':
            return False
        return True

    def setUpTwo(self):
        self.openSettings()
        self.clear_widgets()
        types = ['maps','disease','populations','people']
        self.c = 0
        for type in types:
            self.type = type
            self.displaySettings()
            self.c += 2

        back_button = ttk.Button(self.parent, text='BACK', command=self.back)
        back_button.grid(column=0, row=100, sticky=tk.S)

        simulation_button = ttk.Button(self.parent, text='Start Simulation', command=self.setUpSimulation)
        simulation_button.grid(column=self.c//2, row=100, sticky=tk.S)



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
            data['disease'].append({"name": ["random", 1, "bob", "str"], "transmissionTime": [0.2, 1, 0.1, "float"], "contagion": ["random", 1, 2, "int"], "transmissionRadius": ["random", 1, 2, "int"], "infectedTime": [0.2, 1, 0.2, "float"], "incubationTime": [0.2, 1, 0.2, "float"], "mutation_chance": [0.2, 1, 0.2, "float"]})
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
        self.parent.geometry("1400x540")
        self.parent.resizable(False,False)
        self.setUpTwo()

    def back(self):
        self.cleanUp()
        self.parent.geometry("960x540")
        self.parent.resizable(False,False)

        self.currentIndex = 0
        self.type = 'general'
        self.c = 0
        self.clear_widgets()
        self.setUpOne()

    def setUpOne(self):
        self.openSettings()
        # self.clear_widgets()
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
