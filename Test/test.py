from tkinter import *
from tkinter import ttk
 
def main_change(*args):
    second.set('--None--')
    second['values'] = categories.get(main_selected.get(), ['--None--'])

categories = {'Fruit': ['Apples', 'Grapes', 'Bananas'], 'Vegetables': ['Peas', 'Carrots']}

root = Tk()

main_selected = StringVar()
main_selected.trace('w', main_change)

main = ttk.Combobox(root, values=list(categories.keys()), textvariable=main_selected)
main.pack()
second = ttk.Combobox(root, values=['--None--'])
second.pack()

root.mainloop()