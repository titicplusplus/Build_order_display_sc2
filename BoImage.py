from config_ui import *

import tkinter as tk
from PIL import Image, ImageTk

def StructToPaths(data):
    return f"./image_final/" + data

class BoImage:
    def __init__(self, posi, root, bo, column):
        self.__root  = root
        self.__bo    = bo
        self.__image = tk.Label(root)

        self.__image.grid(row = 0, column = column)
        
        self.__posi   = posi

        self.__time  = tk.Label(root, text="", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__time.grid(row = 1, column = column)

        self.__suply = tk.Label(root, text="", bg=DARK_BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.__suply.grid(row = 2, column = column)

        self.__time.config(font=("Ubuntu Light", 44))
        self.__suply.config(font=("Ubuntu Light", 44))
            
        self.image = None

    def execute(self, open_image=False):
        size  = int((self.__root.winfo_width()/5.0)*0.9)

        if size < 10:
            size = 128

        if open_image == True or self.image == None:
            ctime = ""
            ctext = ""
            
            if self.__posi >= 0 and self.__posi < len(self.__bo):
                self.image = Image.open(StructToPaths(self.__bo[self.__posi][2]))
                
                ctime = self.__bo[self.__posi][0].encode()
                ctext = str(self.__bo[self.__posi][1])
            else:
                self.image = Image.open("./Black.jpg")
                ctime = ""
                ctext = ""
                
            print(self.image.size, (size))

            if self.image.size[0] == self.image.size[1]:
                self.image = self.image.resize((size, size))
            elif self.image.size[0] > self.image.size[1]:
                self.image = self.image.resize((size, int(size*self.image.size[1]/self.image.size[0])))

                nouvelle_image = Image.new("RGB", (size, size), color="black")
                nouvelle_image.paste(self.image, (0, int((size - self.image.size[1])/3)))
                self.image = nouvelle_image
            elif self.image.size[0] < self.image.size[1]:
                self.image = self.image.resize((int(size*self.image.size[0]/self.image.size[1]), size))

                nouvelle_image = Image.new("RGB", (size, size), color="black")
                nouvelle_image.paste(self.image, (int((size - self.image.size[0])/3), 0))
                self.image = nouvelle_image

            self.__time["text"] = ctime
            self.__suply["text"] = ctext
        else:
            self.image.resize((size, size))

        self.current_images = ImageTk.PhotoImage(self.image)
        self.__image.configure(image=self.current_images)


    def advance(self):
        self.__posi += 1
        self.execute(open_image=True)


