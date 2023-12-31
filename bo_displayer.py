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

import json_manip

import main

class ImageChangerApp:
    def resize(self, event):
        if event.widget == self.root and \
           (self.width != event.width or self.height != event.height):
            self.width, self.height = event.width, event.height

            for i in range(len(self.parts)):
                self.parts[i].execute()


    def drawImager(self):
        self.remove_elements()
        self.__starttime = time.time()
        self.width, self.height = self.root.winfo_width(), self.root.winfo_height()
        self.root.bind("<Configure>", self.resize)

        self.parts = [BoImage(i, self.root, self.__bo, i + 3) for i in range(-3, 2)]

        self.change_images()

        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        self.__posi = 0

        self.time_label = tk.Label(self.root, text="0:00", font=("Ubuntu Light", 34), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.time_label.grid(row = 3, column = 2)
        
        self.root.after(50, self.change_images_periodically)  # Change images every 5 seconds
        
        self.__quit = tk.Button(self.root, text="Quit build order", command=self.stop,
                font=("Ubuntu Light", 15), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__quit.grid(row = 3, column=3, pady=10)

    def __init__(self, root, bo):
        self.root = root
        self.__bo = bo
        self.__continue = True

        tk.Label(self.root, text="Press control key to start ! Or press echap to cancel", font=("Ubuntu Light", 34), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR).pack()
        self.root.update_idletasks()  # Force update


        with keyboard.Events() as events:
            for event in events:
                if event.key == keyboard.Key.ctrl_r or event.key == keyboard.Key.ctrl_l:
                    self.drawImager()
                    break
                elif event.key == keyboard.Key.esc:
                    self.cancel()
                    break

    def stop(self):
        self.__continue = False 

    def cancel(self):
        self.remove_elements()
        menu = main.Menu(self.root)

    def remove_elements(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def change_images(self):
        for i in range(len(self.parts)):
            self.parts[i].advance()

    def change_images_periodically(self):
        if not self.__continue:
            self.cancel()
            return

        self.__laspetime = time.time() - self.__starttime
        self.time_label.config(text=f"{int(self.__laspetime//60)}:{int(self.__laspetime%60):02}")
        
        if self.__posi < len(self.__bo):
            #print(self.__bo[self.__posi][0].getTimeSeconds(), self.__laspetime)
            if self.__bo[self.__posi][0].getTimeSeconds() <= self.__laspetime:
                self.change_images()
                self.__posi += 1

        self.root.after(50, self.change_images_periodically)  # Change images every 5 seconds

def openBoFilename(filename):
    lines = ""
    with open(filename, "r") as f:
        lines = f.read().split("\n")

    json_data = json_manip.openJson()
    bo = []
    for line in lines:
        data = line.split(",")


        name = data[3]
        key = json_manip.get_key_from_name(name, json_data)

        ctype = None

        if key == None:
            continue

        print(key)

        if json_data[key]["race"] == 'p':
            if json_data[key]["type"] == 'u':
                ctype = getattr(Protoss.Units, name)
            elif json_data[key]["type"] == 'b':
                ctype = getattr(Protoss.Structure, name)
            elif json_data[key]["type"] == 'p':
                ctype = getattr(Protoss.Upgrade, name)
        elif json_data[key]["race"] == 't':
            if json_data[key]["type"] == 'u':
                ctype = getattr(Terran.Units, name)
            elif json_data[key]["type"] == 'b':
                ctype = getattr(Terran.Structure, name)
            elif json_data[key]["type"] == 'p':
                ctype = getattr(Terran.Upgrade, name)
        elif json_data[key]["race"] == 'z':
            if json_data[key]["type"] == 'u':
                ctype = getattr(Zerg.Units, name)
            elif json_data[key]["type"] == 'b':
                ctype = getattr(Zerg.Structure, name)
            elif json_data[key]["type"] == 'p':
                ctype = getattr(Zerg.Upgrade, name)
        
        #bo[-1][-1] = ctype
        bo.append([BoTime(int(data[1]), int(data[2])), int(data[0]), ctype])


    return bo
