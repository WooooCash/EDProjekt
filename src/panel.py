import codecs
import tkinter as tk
from tkinter import filedialog

from src.data import Data

SEPARATOR_MAPPING = {"Średnik": ";", "Tabulator": "\t", "Spacja": " "}


class Panel(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.structure_label = tk.Label(self, width=20)
        self.structure_label.grid()

        # Narazie tu trzymamy data, ale docelowo nie powinno być w panelu, a w innej częsci
        # w której będziemy faktycznie wyświetlać dane i wykonywać na nich operacje
        self.data = Data()

        # VARS
        header = tk.BooleanVar()
        separator = tk.StringVar(self, " ")

        # UI ELEMENTS
        header_options = tk.Checkbutton(
            self, text="Nagłówek?", variable=header, onvalue=True, offvalue=False
        )
        separator_options = self.__generate_separator_options(separator)
        bt_load = tk.Button(
            self,
            text="Otwórz plik",
            command=lambda: self.__read_data(header.get(), separator.get()),
        )
        bt_debug_data = tk.Button(self, text="Debug", command=lambda: print(self.data))

        # PLACEMENT
        header_options.grid(sticky=tk.EW)
        for option in separator_options:
            option.grid(sticky=tk.EW)
        bt_load.grid(sticky=tk.EW)
        bt_debug_data.grid(sticky=tk.EW)

    def __read_data(self, has_headers: bool, separator: str):
        file = codecs.open(filedialog.askopenfilename(), encoding="utf-8")
        self.data.read_file(file, delimiter=separator, has_headers=has_headers)

    def __generate_separator_options(self, variable: tk.StringVar):
        options_list = []
        for text, value in SEPARATOR_MAPPING.items():
            options_list.append(
                tk.Radiobutton(
                    self,
                    text=text,
                    variable=variable,
                    value=value,
                    background="light blue",
                )
            )

        return options_list
