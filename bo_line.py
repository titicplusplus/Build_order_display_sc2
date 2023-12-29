import tkinter as tk
from tkinter import ttk

from config_ui import *

class BoLine:
    def __init__(self, root, data, line):
        self.data = data
        self.root = root
        self.line = line

        self.ligneLabel = tk.Label(root, text=str(self.line), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        #self.ligneLabel.grid(row=ligne, column=0, sticky="nsew", pady=10)

        self.supplyEntry = tk.Entry(root, width=10, bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                validate="key", validatecommand=(root.register(self.validate_numeric), '%P'))
        #entry.grid(row=ligne, column=1)

        self.minutesEntry = tk.Entry(root, width=10, bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR, justify="right",
                validate="key", validatecommand=(root.register(self.validate_numeric), '%P'))
        #entry.grid(row=ligne, column=2, sticky="e")

        self.pointLabel = tk.Label(root, text=":", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        #entry.grid(row=ligne, column=3, padx=10)

        self.secondsEntry = tk.Entry(root, width=10, bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR,
                validate="key", validatecommand=(root.register(self.validate_numeric), '%P'))
        #entry.grid(row=ligne, column=4, sticky="w")
        
        self.comboboxRace = ttk.Combobox(root, values=["Terran", "Protoss", "Zerg"], state="readonly")
        self.comboboxRace.set("Terran")
        #self.comboboxRace.grid(row=ligne, column=5, sticky="nsew")

        self.comboboxType = ttk.Combobox(root, values=["Buildings", "Units", "Upgrades"], state="readonly")
        self.comboboxType.set("Buildings")
        #self.comboboxType.grid(row=ligne, column=6, sticky="nsew")

        self.comboboxFinal = ttk.Combobox(root, values=[""], state="readonly")
        self.comboboxFinal.set("")
        #self.comboboxFinal.grid(row=ligne, column=7, sticky="nsew")

        self.comboboxRace.bind("<<ComboboxSelected>>", lambda event, \
                combobox=self.comboboxRace: self.selection_changed(event, self.comboboxRace, self.comboboxType, self.comboboxFinal))

        self.comboboxType.bind("<<ComboboxSelected>>", lambda event, \
                combobox=self.comboboxType: self.selection_changed(event, self.comboboxRace, self.comboboxType, self.comboboxFinal))

        self.comboboxRace.bind("<Key>", lambda event, \
                combobox=self.comboboxRace: self.on_key_combo(event, self.comboboxRace, self.comboboxRace, self.comboboxType, self.comboboxFinal))

        self.comboboxType.bind("<Key>", lambda event, \
                combobox=self.comboboxType: self.on_key_combo(event, self.comboboxType, self.comboboxRace, self.comboboxType, self.comboboxFinal))

        self.comboboxFinal.bind("<Key>", lambda event, \
                combobox=self.comboboxFinal: self.on_key_combo(event, self.comboboxFinal, self.comboboxRace, self.comboboxType, self.comboboxFinal))

        self.remove = tk.Button(root, text="Remove Line", command=None,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)

        self.posi()

    def posi(self):
        self.ligneLabel["text"] = str(self.line)
        self.ligneLabel.grid(row=self.line, column=0, sticky="nsew", pady=10)
        self.supplyEntry.grid(row=self.line, column=1, sticky="nsew", pady = 10)
        self.minutesEntry.grid(row=self.line, column=2, sticky="e")
        self.pointLabel.grid(row=self.line, column=3, padx=10)
        self.secondsEntry.grid(row=self.line, column=4, sticky="w")
        self.comboboxRace.grid(row=self.line, column=5, sticky="nsew")
        self.comboboxType.grid(row=self.line, column=6, sticky="nsew")
        self.comboboxFinal.grid(row=self.line, column=7, sticky="nsew")
        self.remove.grid(row=self.line, column=8, padx=10)

    def selection_changed(self, event, comboboxRace, comboboxType, comboboxFinal):
        global data
        print("change !!")
        crace = comboboxRace.get()
        ctype = comboboxType.get()

        if crace not in data.keys() or ctype not in data[crace].keys():
            print(f"Error, {crace} {ctype} not found")
        else:
            comboboxFinal["values"] = data[crace][ctype]
            comboboxFinal.set(data[crace][ctype][0])

    def on_key_combo(self, event, com, comboboxRace, comboboxType, comboboxFinal):
        typed_char = event.char.upper()
        print(f"c: {typed_char}")

        category_options = com["values"]
        matching_categories = [category for category in category_options if category.startswith(typed_char)]
        print(matching_categories, category_options) 

        if matching_categories:
            com.set(matching_categories[0])
            self.selection_changed(None, comboboxRace, comboboxType, comboboxFinal)

    def destroy(self):
        self.ligneLabel.destroy()
        self.supplyEntry.destroy()
        self.minutesEntry.destroy()
        self.pointLabel.destroy()
        self.secondsEntry.destroy()
        self.comboboxRace.destroy()
        self.comboboxType.destroy()
        self.comboboxFinal.destroy()
        self.remove.destroy()


    def validate_numeric(self, value):
        try:
            if value:
                float(value)
            return True
        except ValueError:
            return False

    def getData(self):
        return []

    def getLine(self):
        return self.line

    def setLine(self, line):
        self.line = line
        self.posi()

    def setLineMove(self, move):
        self.line += move
        self.posi()

    def remove_ligne(self):
        pass


