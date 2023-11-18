import tkinter as tk
from tkinter import filedialog
import codecs

from src.data import Data


class Panel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.structure_label = tk.Label(self, width=20)
        self.structure_label.grid()

        # Narazie tu trzymamy data, ale docelowo nie powinno być w panelu, a w innej częsci
        # w której będziemy faktycznie wyświetlać dane i wykonywać na nich operacje
        self.data = Data()
        self.header = tk.BooleanVar()
        self.separator_options = []

        values = {"Średnik": ";",
                  "Tabulator": "\t",
                  "Spacja": " "}
        self.separator = tk.StringVar(self, "1")

        for (text, value) in values.items():
            self.separator_options.append(tk.Radiobutton(self, text=text, variable=self.separator, value=value, background="light blue"))

        header_options = tk.Checkbutton(self, text='Nagłówek?', variable=self.header, onvalue=True, offvalue=False)

        bt_load = tk.Button(self, text="Otwórz plik", command=self.__read_data)
        bt_debug_data = tk.Button(
            self, text="Debug", command=lambda: print(self.data)
        )
        header_options.grid(sticky=tk.EW)
        for option in self.separator_options:
            option.grid(sticky=tk.EW)
        bt_load.grid(sticky=tk.EW)
        bt_debug_data.grid(sticky=tk.EW)

    def __read_data(self):
        file = codecs.open(filedialog.askopenfilename(), encoding='utf-8')

        # parametry delimiter i has_headers trzeba brać z jakiś inputów "Entry"
        self.data.read_file(file, delimiter=str(self.separator), has_headers=bool(self.header))
