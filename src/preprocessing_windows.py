import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Callable

class DiscretizeWindow(tk.Toplevel):
    def __init__(self, parent, col_name: str):
        super().__init__(master=parent)
        self.title(f"Discretize {col_name}")
        self.parent = parent

        bc_label = tk.Label(self, text="Bucket count:")
        self.bc = tk.Entry(self)
        confirm = tk.Button(self, text="Confirm", command=self.__confirm)

        bc_label.grid()
        self.bc.grid()
        confirm.grid()

    def __confirm(self):
        try:
            num_bins = int(self.bc.get())
            self.parent.set_config(num_bins=num_bins)
            self.destroy()
        except ValueError:
            messagebox.showerror("Must be int")
