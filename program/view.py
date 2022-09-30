import tkinter as tk


class UI():
    def __init__(self) -> None:
        self._controller = None

    def register(self, controller):
        self._controller = controller

root= tk.Tk()
root.title('Setup')

canvas1 = tk.Canvas(root, width = 400, height = 300)
canvas1.pack()

OPTIONS = [
"General",
"Disease",
"Population",
"Person",
"Map"
]

variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value


w = tk.OptionMenu(root, variable, *OPTIONS)
canvas1.create_window(200, 180, window=w)
w.pack(side=tk.TOP, anchor=tk.NE)

# label1 = tk.Label(root, text='Settings')
# label1.config(font=('helvetica', 14))
# canvas1.create_window(200, 25, window=label1)

# label2 = tk.Label(root, text='Type your Number:')
# label2.config(font=('helvetica', 10))
# canvas1.create_window(200, 100, window=label2)

# entry1 = tk.Entry (root) 
# canvas1.create_window(200, 140, window=entry1)

button1 = tk.Button(text='Start Simulation', bg='brown', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)
button1.pack(side=tk.BOTTOM, anchor=tk.S)

root.mainloop()
