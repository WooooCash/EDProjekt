import tkinter as tk
from tkinter import messagebox
from typing import Callable

from src.preprocessing import standardize, to_numeric
from src.preprocessing2 import discretize, remap
from src.preprocessing_windows import DiscretizeWindow, RemapWindow
from src.table_frame import Table


class OperationPanel(tk.Frame):
    def __init__(self, parent, table_frame: Table, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.table_frame = table_frame
        self.config = {}

        self.structure_label = tk.Label(self, width=30)
        self.structure_label.grid()

        self.to_numeric_button = tk.Button(
            self,
            text="To numeric",
            # command=lambda: print(self.table_frame.sheet.get_selected_columns()),
            command=lambda: self.__immediate(to_numeric),
        )

        self.discretize_button = tk.Button(
            self,
            text="Discretize",
            # command=lambda: print(self.table_frame.sheet.get_selected_columns()),
            command=lambda: self.__window_op(discretize, DiscretizeWindow),
        )

        self.standardize_button = tk.Button(
            self,
            text="Standardize",
            # command=lambda: print(self.table_frame.sheet.get_selected_columns()),
            command=lambda: self.__immediate(standardize),
        )

        self.remap_button = tk.Button(
            self,
            text="Map",
            # command=lambda: print(self.table_frame.sheet.get_selected_columns()),
            command=lambda: self.__window_op(remap, RemapWindow),
        )

        self.to_numeric_button.grid(sticky=tk.EW)
        self.discretize_button.grid(sticky=tk.EW)
        self.standardize_button.grid(sticky=tk.EW)
        self.remap_button.grid(sticky=tk.EW)

    def set_config(self, **kwargs):
        self.config = kwargs

    def __immediate(self, func: Callable):
        cols = self.table_frame.get_selected_cols()
        if len(cols) != 1:
            messagebox.showerror("Error", "One (only one) column must be selected")
            return

        col_idx = cols[0]
        column, _ = self.__get_col(col_idx)

        new_col = func(column, {})
        self.table_frame.set_column(col_idx, new_col)

    def __window_op(self, func: Callable, window_class):
        cols = self.table_frame.get_selected_cols()
        if len(cols) != 1:
            messagebox.showerror("Error", "One (only one) column must be selected")
            return

        col_idx = cols[0]
        column, header = self.__get_col(col_idx)

        popup = window_class(self, header)

        self.wait_window(popup)

        new_col = func(column, self.config)
        self.table_frame.set_column(col_idx, new_col)

    def __get_col(self, idx):
        col = self.table_frame.data.cols[idx]
        header = self.table_frame.data.headers[idx]
        return col, header

    def __get_valid_col_selection(self) -> int:
        cols = self.table_frame.get_selected_cols()
        if len(cols) != 1:
            messagebox.showerror("One (only one) column must be selected", "Error")
            return -1

        return cols[0]
