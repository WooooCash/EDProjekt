import tkinter as tk
from tkinter import messagebox

class DiscretizeWindow(tk.Toplevel):
    def __init__(self, parent, col_name: str):
        super().__init__(master=parent)
        self.title(f"TK_ED - Discretize {col_name}")
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
            messagebox.showerror("Error", "Must be int")

class RemapWindow(tk.Toplevel):
    def __init__(self, parent, col_name: str):
        super().__init__(master=parent)
        self.title(f"TK_ED - Map {col_name}")
        self.parent = parent

        a_label = tk.Label(self, text="Lower bound")
        self.a = tk.Entry(self)

        b_label = tk.Label(self, text="Upper bound")
        self.b = tk.Entry(self)
        confirm = tk.Button(self, text="Confirm", command=self.__confirm)

        a_label.grid()
        self.a.grid()
        b_label.grid()
        self.b.grid()
        confirm.grid()

    def __confirm(self):
        try:
            a = float(self.a.get())
            b = float(self.b.get())
            self.parent.set_config(a=a, b=b)
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Must be number")
