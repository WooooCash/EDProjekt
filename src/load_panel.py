import codecs
import tkinter as tk
from tkinter import filedialog

from src.data import Data
from src.table_frame import Table

SEPARATOR_MAPPING = {"Średnik": ";", "Tabulator": "\t", "Spacja": " "}


class LoadPanel(tk.Frame):
    def __init__(self, parent, table_frame: Table, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.table_frame = table_frame

        self.structure_label = tk.Label(self, width=30)
        self.structure_label.grid()

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

        # PLACEMENT
        header_options.grid(sticky=tk.EW)
        for option in separator_options:
            option.grid(sticky=tk.EW)
        bt_load.grid(sticky=tk.EW)

    def __read_data(self, has_headers: bool, separator: str):
        self.table_frame.load_file(has_headers, separator)

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
