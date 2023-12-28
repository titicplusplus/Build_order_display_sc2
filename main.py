import tkinter as tk

# from ttkthemes import ThemedTk

from pynput import keyboard
from tkinter import font

import time

from sc2_elements import *
import json
import os

from BoTime import *
from BoImage import *
from config_ui import *

class ImageChangerApp:
    def resize(self, event):
        if event.widget == self.root and \
           (self.width != event.width or self.height != event.height):
            self.width, self.height = event.width, event.height

            for i in range(len(self.parts)):
                self.parts[i].execute()


    def __init__(self, root, bo):
        self.__starttime = time.time()
        self.__bo = bo
        self.root = root
        self.width, self.height = self.root.winfo_width(), self.root.winfo_height()
        root.bind("<Configure>", self.resize)

        self.parts = [BoImage(i, root, bo, i + 3) for i in range(-3, 2)]

        self.change_images()

        # Configuration des lignes et colonnes pour qu'elles s'étendent
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        self.__posi = 0

        self.time_label = tk.Label(self.root, text="0:00", font=("Ubuntu Light", 34), bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.time_label.grid(row = 3, column = 2)
        
        self.root.after(50, self.change_images_periodically)  # Change images every 5 seconds

    def change_images(self):
        for i in range(len(self.parts)):
            self.parts[i].advance()

    def change_images_periodically(self):
        self.__laspetime = time.time() - self.__starttime
        self.time_label.config(text=f"{int(self.__laspetime//60)}:{int(self.__laspetime%60):02}")
        
        if self.__posi < len(self.__bo):
            #print(self.__bo[self.__posi][0].getTimeSeconds(), self.__laspetime)
            if self.__bo[self.__posi][0].getTimeSeconds() <= self.__laspetime:
                self.change_images()
                self.__posi += 1

        self.root.after(50, self.change_images_periodically)  # Change images every 5 seconds


def openJson():
    data = {}
    with open("output.json", 'r') as json_file:
        data = json.load(json_file)
    return data

def openFilename(filename):
    lines = ""
    with open(filename, "r") as f:
        lines = f.read().split("\n")

    json_data = openJson()
    bo = []
    for line in lines:
        data = line.split(",")
        if len(data) != 3:
            print("Error, size not correct :", data)
            continue

        bo.append([BoTime(int(data[1][:data[1].find(":")]), int(data[1][data[1].find(":") + 1:])), int(data[0]), None])
        key = data[2]
        name = json_data[key]["name"]

        ctype = None

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
        bo[-1][-1] = ctype

    return bo

def openBo():
    bos = [files for files in os.listdir("./") if files[-4:] == ".csv"]
    dictbos = {}

    print("Select your bo (enter touch): ")
    for i in range(len(bos)):
        print(f"{chr(97 + i)} : {bos[i]}")
        dictbos[ chr(97 + i) ] = bos[i]

    print("Key seletecd: ")
    filename = ""
    with keyboard.Events() as events:
        for event in events:
            key = str(event.key)
            if len(key) == 3:
                key = key[1]

                if key in dictbos.keys():
                    filename = dictbos[key]
                    break

    print("")

    return openFilename(filename), filename



def on_key_release(key):
    if key == keyboard.Key.ctrl_r:
        return False

if __name__ == "__main__":
    
    bo, filename = openBo()

    print("Wait for key ctrl right to start")
    with keyboard.Listener(on_release=on_key_release) as listener:
        listener.join()

    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # replace either screen_width and screen_height to change the appropriate dimension
    root.geometry(f"{screen_width}x{screen_height}")
    root.configure(bg=DARK_BACKGROUND_COLOR)

    root.title(filename)
    app = ImageChangerApp(root, bo)
    root.mainloop()
