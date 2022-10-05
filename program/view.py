import os 
import json
import tkinter as tk
from tkinter import ttk

class UI():
    def __init__(self) -> None:
        self._controller = None


    def register(self, controller):
        self._controller = controller
    

    def mainloop(self):
        a = input('>> ')
        if a == '1':
            self._controller.pauseSimulation()


    def setUpSimulation(self):
        self._controller.setUpSimulationData()


"""
main menu which is the general collumns then you have sub menus so if 2 diseases it will created d1 d2 in sub menu 
"""
class App(tk.Tk):
    def __init__(self):
        super().__init__()
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

        # create widget
        self.create_wigets()

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
        
        button = ttk.Button(self, text='Start Simulation')
        button.grid(column=1, row=100, sticky=tk.S, **paddings)
    

    def updateSettings(self) -> None:
        paddings = {'padx': 5, 'pady': 5}
        with open(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/createTools/settings.json'),'r') as file:
            data = json.load(file)
        
        i = 0
        for key in data[self.type]:
            if  self.vs[i].get() == 1:
                data[self.type][key][1] = 1
                data[self.type][key][0] = "random"
            else:
                data[self.type][key][1] = 0
                data[self.type][key][0] = self.e[i].get()
            i+=1

        with open(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/createTools/settings.json'),'w') as file:
            json.dump(data, file)
        
        self.output_label.destroy()
        self.output_label = ttk.Label(self, foreground='green',text='changes have been applied')
        self.output_label.grid(column=0, row=100, sticky=tk.W, **paddings)


    def verification(self):
        paddings = {'padx': 5, 'pady': 5}
        with open(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/createTools/settings.json'),'r') as file:
            data = json.load(file)

        values = [i.get() for i in self.e] 
        try:
            i = 0
            for key in data[self.type]:
                if self.vs[i].get() == 0:
                    if data[self.type][key][1] == 0:
                        i+=1
                    elif data[self.type][key][1] == 1 and (values[i] == "random" or data[self.type][key][0] == "random"):
                        i+=1
                elif data[self.type][key][3] == "str":
                    if isinstance(values[i], str):
                        i+=1
                elif data[self.type][key][3] == "float":
                    print(values[i])
                    if isinstance(float(values[i]), float):
                        i+=1
                elif data[self.type][key][3] == "int":
                    if isinstance(int(values[i]), int):
                        i+=1
            self.updateSettings()
        except:
            self.output_label.destroy()
            self.output_label = ttk.Label(self, foreground='red',text='incorrect type/s')
            self.output_label.grid(column=0, row=100, sticky=tk.W, **paddings)

    def displaySettings(self, *args):
        paddings = {'padx': 5, 'pady': 5}

        with open(os.path.expanduser('~/Documents/NEA/NEA_CODE/program/createTools/settings.json'),'r') as file:
            data = json.load(file)

        i = 0
        r = 1
        self.e = []
        self.l = []
        self.r = []
        self.vs = []
        for key, value in data[self.type].items():
            self.vs.append(tk.IntVar())
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
            checkbutton = tk.Checkbutton(self, onvalue = 1, offvalue = 0,variable=self.vs[i], text='Randomise')
            checkbutton.grid(column=4, row=r, sticky=tk.W,**paddings)
            self.r.append(checkbutton)
            i += 1
            r+=1

        self.button2 = ttk.Button(self, text='Commit', command=self.verification)
        self.button2.grid(column=1, row=r, sticky=tk.S, **paddings)
    

    def option_changed(self, *args):
        if self.type != None:
            for label in self.l:
                label.destroy()
            for entry in self.e:
                entry.destroy()
            for checkbutton in self.r:
                checkbutton.destroy()
            self.button2.destroy()
            
        if self.option_var.get() == 'General':
            self.type = "general"
            self.displaySettings()
        elif self.option_var.get() == 'Disease':
            self.type = "disease"
            self.displaySettings()
        elif self.option_var.get() == 'Population':
            self.type = "populations"
            self.displaySettings()
        elif self.option_var.get() == 'Person':
            self.type = "people"
            self.displaySettings()
        elif self.option_var.get() == 'Map':
            self.type = "maps"
            self.displaySettings()


if __name__ == "__main__":
    app = App()
    app.mainloop()