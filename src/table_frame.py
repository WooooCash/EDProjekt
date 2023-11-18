import codecs
import tkinter as tk
from tkinter.filedialog import askopenfilename

from tksheet import Sheet

from src.data import Data

BINDINGS = ["single_select", "column_select", "row_select", "prior", "next"]


class Table(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.data = Data()

        self.sheet = Sheet(self)
        self.sheet.enable_bindings(*BINDINGS)
        self.sheet.grid()

    def load_file(self, has_headers: bool, separator: str):
        file = codecs.open(askopenfilename(), encoding="utf-8")
        self.data.read_file(file, delimiter=separator, has_headers=has_headers)
        self.__set_table_contents()

    def __set_table_contents(self):
        self.sheet.headers(self.data.headers)
        self.sheet.set_sheet_data(self.data.as_rows())
