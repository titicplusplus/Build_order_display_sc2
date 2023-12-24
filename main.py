import tkinter as tk
from PIL import Image, ImageTk

from pynput import keyboard

import time

from sc2_elements import *

def StructToPaths(data):
    return f"./image_final/" + data

class BoTime:
    def __init__(self, minutes, seconds):
        self.__minutes = minutes
        self.__seconds = seconds

    def parse(self, data):
        spliter = data.split(":")

        self.__seconds = int(spliter[0])
        self.__minutes = int(spliter[1])

    def encode(self):
        flux = ""

        if self.__minutes < 10:
            flux += "0"
        flux += str(self.__minutes) + ":"

        if self.__seconds < 10:
            flux += "0"
        flux += str(self.__seconds)

        return flux

    def getTime(self):
        return (self.__minutes, self.__seconds)

    def getTimeSeconds(self):
        return self.__minutes*60 + self.__seconds

def diffBoTime(t1, t2):
    m1, s1 = t1.getTime()
    m2, s2 = t2.getTime()

    total1 = m1*60 + s1
    total2 = m2*60 + s2

    return total2 - total1



class BoImage:
    def __init__(self, posi, root, bo, column):
        self.__root  = root
        self.__bo    = bo
        self.__image = tk.Label(root)

        self.__image.grid(row = 0, column = column, sticky="nsew")
        
        self.__posi   = posi

        self.__time  = tk.Label(root, text="")
        self.__time.grid(row = 1, column = column, sticky="nsew")

        self.__suply = tk.Label(root, text="")
        self.__suply.grid(row = 2, column = column, sticky="nsew")

        self.__time.config(font=("Courier", 44))
        self.__suply.config(font=("Courier", 44))

    def execute(self):
        #print(self.__root.winfo_width(), self.__root.winfo_height())

        size  = int((self.__root.winfo_width()/5.0)*0.9)

        if size < 10:
            size = 128

        image = None
        ctime = ""
        ctext = ""

        
        if self.__posi >= 0 and self.__posi < len(self.__bo):
            image = Image.open(StructToPaths(self.__bo[self.__posi][2]))
            
            ctime = self.__bo[self.__posi][0].encode()
            ctext = str(self.__bo[self.__posi][1])
        else:
            image = Image.open("../CppPart/image/Black.jpg")
            #self.current_images = ImageTk.PhotoImage(image)
            #self.__image.configure(image=self.current_images)
            ctime = ""
            ctext = ""
            
        image = image.resize((size, size))
        self.current_images = ImageTk.PhotoImage(image)
        self.__image.configure(image=self.current_images)

        self.__time["text"] = ctime
        self.__suply["text"] = ctext

    def advance(self):
        self.__posi += 1
        self.execute()



class ImageChangerApp:
    def resize(self, event):
        if event.widget == self.root and \
           (self.width != event.width or self.height != event.height):
            print(f'{event.height=}, {event.width=}')

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

        self.time_label = tk.Label(self.root, text="0:00:00", font=("Helvetica", 24))
        self.time_label.grid(row = 3, column = 2)
        
        self.root.after(50, self.change_images_periodically)  # Change images every 5 seconds

    def change_images(self):
        for i in range(len(self.parts)):
            self.parts[i].advance()

    def change_images_periodically(self):
        #self.change_images()
        #if self.__posi + 1 < len(self.__bo):
        #    self.root.after(diffBoTime(self.__bo[self.__posi][0], self.__bo[self.__posi + 1][0])*1000, self.change_images_periodically)
        #    print(diffBoTime(self.__bo[self.__posi][0], self.__bo[self.__posi + 1][0]))
        #    self.__posi += 1

        self.__laspetime = time.time() - self.__starttime
        self.time_label.config(text=f"{int(self.__laspetime//60)}:{int(self.__laspetime%60):02}")
        
        if self.__posi < len(self.__bo):
            #print(self.__bo[self.__posi][0].getTimeSeconds(), self.__laspetime)
            if self.__bo[self.__posi][0].getTimeSeconds() <= self.__laspetime:
                self.change_images()
                self.__posi += 1

        self.root.after(50, self.change_images_periodically)  # Change images every 5 seconds


bo1 = [
        [BoTime(0, 2), 21, Terran.Structure.Barracks], # [(minutes, seconds), supply, type]
        [BoTime(0, 8), 25, Terran.Structure.Starport],
        [BoTime(0, 18), 28, Terran.Structure.Sensor_tower],
        [BoTime(0, 24), 28, Terran.Structure.Barracks],
        [BoTime(0, 34), 28, Terran.Structure.Reactor],
        [BoTime(0, 44), 28, Terran.Structure.Tech_Lab],
        [BoTime(0, 44), 28, Terran.Units.Marine],
        [BoTime(1, 12), 29, Terran.Upgrade.StimPack],
        [BoTime(1, 13), 29, Terran.Upgrade.Infantry_Armor],
]

def on_key_release(key):
    if key == keyboard.Key.ctrl_r:
        return False

if __name__ == "__main__":
    print("Wait for key ctrl right to start")
    with keyboard.Listener(on_release=on_key_release) as listener:
        listener.join()

    root = tk.Tk()
    root.title("Image Changer App")
    app = ImageChangerApp(root, bo1)                    # C'est ici que tu mets le bo
    root.mainloop()
