import tkinter as tk

from tkinter import scrolledtext
import LotvToBo

class ImportLotvBo(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)

        input_box_label = tk.Label(self, text="The build order:")
        input_box_label.pack()

        self.input_box = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.input_box.pack(fill=tk.BOTH, expand=True, pady=10)

        execute_button = tk.Button(self, text="Execute", command=self.execute)
        execute_button.pack()

        cancel_button = tk.Button(self, text="Cancel", command=self.cancel)
        cancel_button.pack()

        self.result = None

    def execute(self):
        self.result = LotvToBo.execute_code(self.input_box.get("1.0", "end-1c"))
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()
