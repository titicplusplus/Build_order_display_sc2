import tkinter as tk
from tkinter import ttk

import platform

from config_ui import *

class ScrollableFrame(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        
        # Créez une zone de défilement
        self.canvas = tk.Canvas(self, borderwidth=0, background=DARK_BACKGROUND_COLOR)
        self.frame = tk.Frame(self.canvas, background=DARK_BACKGROUND_COLOR)

        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, width=30, bg=DARK_BACKGROUND_COLOR)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview, width=30, bg=DARK_BACKGROUND_COLOR)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4,4), window=self.frame, anchor="n", 
                                                      tags="self.frame")
        

        self.frame.bind("<Configure>", self.onFrameConfigure)


        for i in range(1, 8):
            self.frame.grid_columnconfigure(i, weight=1)
        self.frame.grid_columnconfigure(3, weight=0)

        self.onFrameConfigure(None)

        self.canvas.bind("<Configure>", self.resize_frame)

    def addLegend(self):
        tk.Label(self.frame, text=" n° line", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR) \
            .grid(row=0, column=0, sticky="nsew", pady=10)

        tk.Label(self.frame, text="Supply", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR) \
            .grid(row=0, column=1, sticky="nsew")

        tk.Label(self.frame, text="Time 'min:sec'", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR) \
            .grid(row=0, column=2, sticky="e")

        tk.Label(self.frame, text="Choose race", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR) \
            .grid(row=0, column=5, sticky="w")

        tk.Label(self.frame, text="Choose type", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR) \
            .grid(row=0, column=6, sticky="w")

        tk.Label(self.frame, text="Choose elements", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR) \
            .grid(row=0, column=7, sticky="w")
        
        self.onFrameConfigure(None)

    def resize_frame(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width*0.99)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def upMouseWheel(self, event):
        self.canvas.yview_scroll(-1, "units")

    def downMouseWheel(self, event):
        self.canvas.yview_scroll(1, "units")

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface Graphique")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Première partie avec un label et une entry pour le nom du fichier
        self.__boname = tk.Label(root, text="Bo's name : ", font=("Ubuntu Light", 20), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__boname.grid(row=0, column=0, sticky="e")

        self.__filename_entry = tk.Entry(root)
        self.__filename_entry.grid(row=0, column=1, pady=50)

        # Deuxième partie avec une zone de défilement contenant les widgets
        self.__scrollable_frame = ScrollableFrame(root)
        self.__scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=20, padx=20)

        # Troisième partie avec un bouton "Ajouter"
        self.__addline = tk.Button(root, text="Ajouter", command=self.ajouter_ligne,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__addline.grid(row=2, column=0, pady=10)

        # Quatrième partie avec un bouton "Import from lotv"
        self.__import = tk.Button(root, text="Import from lotv", command=self.importer_lotv,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__import.grid(row=2, column=1, pady=20)

        
        if platform.system() == 'Linux':
            self.root.bind_all("<Button-4>", self.__scrollable_frame.upMouseWheel)
            self.root.bind_all("<Button-5>", self.__scrollable_frame.downMouseWheel)
        else:
            self.root.bind_all("<MouseWheel>", self.__scrollable_frame.onMouseWheel)
        

    def addLegend(self):
        self.__scrollable_frame.addLegend()

    def ajouter_ligne(self):
        # Ajoutez une nouvelle ligne à la zone de défilement
        ligne = len(self.__scrollable_frame.frame.grid_slaves()) // 7 + 1

        # Numéro de ligne
        tk.Label(self.__scrollable_frame.frame, text=str(ligne), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR) \
            .grid(row=ligne, column=0, sticky="nsew", pady=10)

        entry = tk.Entry(self.__scrollable_frame.frame, width=10, bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                validate="key", validatecommand=(root.register(self.validate_numeric), '%P'))
        entry.grid(row=ligne, column=1)

        entry = tk.Entry(self.__scrollable_frame.frame, width=10, bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR, justify="right",
                validate="key", validatecommand=(root.register(self.validate_numeric), '%P'))
        entry.grid(row=ligne, column=2, sticky="e")

        entry = tk.Label(self.__scrollable_frame.frame, text=":", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        entry.grid(row=ligne, column=3, padx=10)

        entry = tk.Entry(self.__scrollable_frame.frame, width=10, bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR,
                validate="key", validatecommand=(root.register(self.validate_numeric), '%P'))
        entry.grid(row=ligne, column=4, sticky="w")
        
        # Combobox
        
        combobox = ttk.Combobox(self.__scrollable_frame.frame, values=["Terran", "Protoss", "Zerg"])
        combobox.set("Terran")  # Définissez la valeur par défaut si nécessaire
        combobox.grid(row=ligne, column=col, sticky="nsew")

        # Ajustez la taille de la zone de défilement
        self.__scrollable_frame.onFrameConfigure(None)

    def validate_numeric(self, value):
        try:
            if value:
                float(value)
            return True
        except ValueError:
            return False


    def importer_lotv(self):
        # Logique pour importer depuis lotv
        print("Import depuis lotv")

if __name__ == "__main__":
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"{screen_width}x{screen_height}")
    root.configure(bg=DARK_BACKGROUND_COLOR)

    app = Application(root)
    app.addLegend()
    root.mainloop()
