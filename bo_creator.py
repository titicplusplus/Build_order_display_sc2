import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

import platform
#import open_data

import bo_line as BoLine
import csv_files

from config_ui import *
from ImportLotv import *

from bo_delete import *
from bo_ask_save import *
import os

import json_manip
import main

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
    def __init__(self, root, data, dataRace, text="", filename=""):
        self.data = data
        self.dataRace = dataRace
        self.root = root
        self.root.title("Interface Graphique")

        self.root.grid_rowconfigure(1, weight=1)

        for i in range(0, 5):
            self.root.grid_columnconfigure(i, weight=1)

        # 
        self.__boname = tk.Label(root, text="Build order name : ", font=("Ubuntu Light", 20), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__boname.grid(row=0, column=0, columnspan=2, sticky="e", pady=50)


        self.__filename_entry = tk.Entry(root, text=text)
        self.__filename_entry.grid(row=0, column=2, columnspan=2, padx=10, pady=40, sticky="nsew")
        self.__filename_entry.configure(font=font.Font(size=16))

        self.__filename_entry.delete(0, tk.END)
        self.__filename_entry.insert(0, text)

        self.__quit  = tk.Button(root, text="Quit", command=self.quit,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__quit.grid(row=0, column=4, pady=10)


        #
        self.__scrollable_frame = ScrollableFrame(root)
        self.__scrollable_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", pady=20, padx=20)

        #
        self.__addline = tk.Button(root, text="Add line", command=self.ajouter_ligne,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__addline.grid(row=2, column=0, pady=10)
        
        self.__sort    =  tk.Button(root, text="Sort by time", command=self.sorts_lines,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__sort.grid(row=2, column=1, pady=10)

        self.__save    =  tk.Button(root, text="Save build order", command=self.save,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__save.grid(row=2, column=2, pady=10)

        #
        self.__import = tk.Button(root, text="Import from lotv", command=self.importer_lotv,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__import.grid(row=2, column=3, pady=20)

        self.__delete =  tk.Button(root, text="Delete build order", command=self.remove_bo,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__delete.grid(row=2, column=4, pady=10)
        
        if platform.system() == 'Linux':
            self.root.bind_all("<Button-4>", self.__scrollable_frame.upMouseWheel)
            self.root.bind_all("<Button-5>", self.__scrollable_frame.downMouseWheel)
        else:
            self.root.bind_all("<MouseWheel>", self.__scrollable_frame.onMouseWheel)

        self.boLine = []

        if filename != "":
            self.open_filename(filename)

    def addLegend(self):
        self.__scrollable_frame.addLegend()

    def ajouter_ligne(self):
        self.boLine.append(BoLine.BoLine(self.__scrollable_frame.frame, self.dataRace, len(self.boLine) + 1))

        posi = len(self.boLine) - 1
        self.boLine[-1].remove.config(command=lambda: self.remove_element(posi))
        self.__scrollable_frame.onFrameConfigure(None)

    def remove_element(self, i):
        self.boLine[i].destroy()
        self.boLine.pop(i)
        
        for j in range(i, len(self.boLine)):
            self.boLine[j].setLineMove(-1)

        for j in range(0, len(self.boLine)):
            self.boLine[j].remove.config(command=lambda: self.remove_element(j))

        self.__scrollable_frame.onFrameConfigure(None)

    def sorts_lines(self):
        self.boLine.sort(key = lambda bo: bo.getTime())

        for j in range(0, len(self.boLine)):
            self.boLine[j].remove.config(command=lambda: self.remove_element(j))
            self.boLine[j].setLine(j + 1)

    def save(self):
        if len(self.__filename_entry.get()) == 0:
            messagebox.showerror("Erreur", "Please enter a build order name")
            return

        self.sorts_lines()
        data = []

        for i in range(len(self.boLine)):
            data.append(self.boLine[i].getData())

            if data[i][1] == "" or data[i][2] == "" or data[i][3] == "":
                messagebox.showerror("Erreur", f"Please, complete the {i+1} line.")
                return

        csv_files.export_bo_creator(data, self.__filename_entry.get())
        messagebox.showinfo("Information", "The build order is saved !")

    def importer_lotv(self):
        dialog = ImportLotvBo(self.root, "Import Lotv build order")
        self.root.wait_window(dialog)

        if dialog.result is not None:
            #print("ui")
            #print(dialog.result)

            for line in dialog.result:
                self.boLine.append(BoLine.BoLine(self.__scrollable_frame.frame, self.dataRace, len(self.boLine) + 1))

                posi = len(self.boLine) - 1
                self.boLine[-1].remove.config(command=lambda: self.remove_element(posi))
                self.boLine[-1].setData(line)
            self.__scrollable_frame.onFrameConfigure(None)
            self.sorts_lines()

    def open_filename(self, filename):
        lines = ""
        with open(filename, "r") as f:
            lines = f.read().split("\n")

        for line in lines:
            d = line.split(",")

            key = json_manip.get_key_from_name(d[3], self.data)

            d[3] = [self.data[key]["name"], self.data[key]["race"], self.data[key]["type"]]

            self.boLine.append(BoLine.BoLine(self.__scrollable_frame.frame, self.dataRace, len(self.boLine) + 1))
            posi = len(self.boLine) - 1
            self.boLine[-1].remove.config(command=lambda: self.remove_element(posi))
            self.boLine[-1].setData(d)
        self.__scrollable_frame.onFrameConfigure(None)




    def remove_bo(self):
        dialog = DeleteBo(self.root)
        self.root.wait_window(dialog)

        if dialog.result == True:
            if os.path.exists("./config_bo/" + self.__filename_entry.get() + ".csv"):
                print("remove")
                os.remove("./config_bo/" + self.__filename_entry.get() + ".csv")
            else:
                print(f"file doesn't exsits: ./config_bo/{self.__filename_entry.get()}.csv")

            self.remove_elements()
            menu = main.Menu(self.root)

    def remove_elements(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def quit(self):
        dialog = SaveBo(self.root)
        self.root.wait_window(dialog)

        if dialog.result == True:
            self.save()

        self.remove_elements()
        menu = main.Menu(self.root)




if __name__ == "__main__":
    #data = json_manip.make_data()

    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.configure(bg=DARK_BACKGROUND_COLOR)

    app = Application(root, json_manip.openJson(), json_manip.make_data(), text="test", filename="config_bo/test.csv")
    app.addLegend()
    root.geometry(f"{screen_width}x{screen_height}")
    root.mainloop()
