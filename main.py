import tkinter as tk

from pynput import keyboard
from tkinter import font

import time

from sc2_elements import *
import json
import os

from BoTime import *
from BoImage import *
from config_ui import *

import os

import bo_creator
import bo_displayer

import json_manip

class Menu:
    def __init__(self, root):
        self.root = root
        self.draw_elements()

    def draw_elements(self):
        self.__run = tk.Button(self.root, text="Run a build order", command=self.runBuild, padx=40, pady=20,
                font=("Ubuntu Light", 20), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__run.pack(padx=10, pady=10, expand=True)

        self.__open_bo = tk.Button(self.root, text="Edit a build order", command=self.openBo, padx=40, pady=20,
                font=("Ubuntu Light", 20), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__open_bo.pack(padx=10, pady=10, expand=True)

        self.__create_bo = tk.Button(self.root, text="Create a build order", command=self.createBo, padx=40, pady=20,
                font=("Ubuntu Light", 20), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__create_bo.pack(padx=10, pady=10, expand=True)

        self.root.bind("<Configure>", self.nothing)

    def nothing(self, event):
        pass

    def remove_elements(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def get_files(self):
        self.__buttons = []

        self.files = os.listdir("./config_bo/")

        tk.Label(self.root, text="Choose the build order", font=("Ubuntu Light", 20), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR) \
            .pack(pady=100)

        if self.files:
            scrollbar = tk.Scrollbar(self.root, orient="vertical")

            canvas = tk.Canvas(self.root, borderwidth=10, background=DARK_BACKGROUND_COLOR, yscrollcommand=scrollbar.set)
            canvas.pack(side="top", fill="both", expand=True)

            scrollbar.config(command=canvas.yview)
            scrollbar.pack(side="right", fill="y")

            frame = tk.Frame(canvas, background=DARK_BACKGROUND_COLOR)
            canvas.create_window((5, 5), window=frame, anchor="center")

            screen_width = self.root.winfo_screenwidth()

            for i, filename in enumerate(self.files):
                self.__buttons.append(tk.Button(frame, text=filename[0:-4], command=lambda param=i: self.chooseFiles(param), padx=40, pady=20, width=100,
                    font=("Ubuntu Light", 20), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR))
                self.__buttons[-1].pack(pady=50, padx=100, side="top")

            frame.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        else:
            tk.Label(self.root, text="Please create a build order (cancel -> create new build order)",
                    font=("Ubuntu Light", 20), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR) \
                .pack(pady=100)

        self.__cancel = tk.Button(self.root, text="Cancel", command=self.cancel, padx=40, pady=20, width=100,
            font=("Ubuntu Light", 20), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__cancel.pack(pady=30, side="bottom")

    def cancel(self):
        self.remove_elements()
        self.draw_elements()

    def runBuild(self):
        self.remove_elements()
        self.get_files()
        self.typeW = "RUN"

    def openBo(self):
        self.remove_elements()
        self.get_files()
        self.typeW = "OPEN"

    def createBo(self):
        self.remove_elements()

        app = bo_creator.Application(self.root, json_manip.openJson(), json_manip.make_data())
        app.addLegend()

    def chooseFiles(self, i):
        self.remove_elements()

        if self.typeW == "OPEN":
            app = bo_creator.Application(self.root, json_manip.openJson(), json_manip.make_data(), text=self.files[i][0:-4], filename="config_bo/" + self.files[i])
            app.addLegend()
        elif self.typeW == "RUN":
            bo = bo_displayer.openBoFilename("config_bo/" + self.files[i])
            app = bo_displayer.ImageChangerApp(self.root, bo)


def main():
    root = tk.Tk()

    root.title("Build Order displayer")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    root.geometry(f"{screen_width}x{screen_height}")
    root.configure(bg=DARK_BACKGROUND_COLOR)

    menu = Menu(root)

    root.mainloop()


if __name__ == "__main__":
    main()
