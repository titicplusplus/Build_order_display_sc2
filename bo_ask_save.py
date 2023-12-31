import tkinter as tk
from tkinter import ttk

class SaveBo(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Save build order")

        tk.Label(self, text="Do you want to save the build order ?").pack(pady=10)

        tk.Button(self, text="Yeah, save it", command=self.on_ok_button).pack(side=tk.LEFT, padx=10)
        tk.Button(self, text="no", command=self.on_cancel_button).pack(side=tk.RIGHT, padx=10)

    def on_ok_button(self):
        self.result = True
        self.destroy()

    def on_cancel_button(self):
        self.result = False
        self.destroy()
