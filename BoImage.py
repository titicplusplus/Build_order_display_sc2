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

    def execute(self):
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
            image = Image.open("./Black.jpg")
            ctime = ""
            ctext = ""
            
        print(image.size, (size))

        if image.size[0] == image.size[1]:
            image = image.resize((size, size))
        elif image.size[0] > image.size[1]:
            image = image.resize((size, int(size*image.size[1]/image.size[0])))

            nouvelle_image = Image.new("RGB", (size, size), color="black")
            nouvelle_image.paste(image, (0, int((size - image.size[1])/3)))
            image = nouvelle_image
        elif image.size[0] < image.size[1]:
            image = image.resize((int(size*image.size[0]/image.size[1]), size))

            nouvelle_image = Image.new("RGB", (size, size), color="black")
            nouvelle_image.paste(image, (int((size - image.size[0])/3), 0))
            image = nouvelle_image

        self.current_images = ImageTk.PhotoImage(image)
        self.__image.configure(image=self.current_images)

        self.__time["text"] = ctime
        self.__suply["text"] = ctext

    def advance(self):
        self.__posi += 1
        self.execute()


