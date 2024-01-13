import tkinter as tk
from tkinter import messagebox
from src.col_choice_window import ColChoice
from src.preprocessing2 import plot_2d

from src.table_frame import Table


class VisualPanel(tk.Frame):
    def __init__(self, parent, table_frame: Table, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.table_frame = table_frame

        self.structure_label = tk.Label(self, width=30)
        self.structure_label.grid()

        self.graph_2d_button = tk.Button(
            self,
            text="Graph 2d",
            command=self.visualize_2d
        )
        self.graph_3d_button = tk.Button(
            self,
            text="Graph 3d",
        )
        self.histogram_button = tk.Button(
            self,
            text="Histogram",
        )

        self.graph_2d_button.grid(sticky=tk.EW)
        self.graph_3d_button.grid(sticky=tk.EW)
        self.histogram_button.grid(sticky=tk.EW)

    def visualize_2d(self):
        cols = self.table_frame.get_selected_cols()
        if len(cols) != 3:
            messagebox.showerror("Error", "Must select at 3 columns")
            return

        data_headers = self.__get_header_list()
        headers = {i: data_headers[i] for i in cols}
        classifier = tk.IntVar(self)
        choice_window = ColChoice(headers, classifier)
        self.wait_window(choice_window)
        class_col_idx = classifier.get()

        attr_cols, class_col = self.__get_cols(cols, class_col_idx)
        plot_2d(attr_cols[0], attr_cols[1], class_col)

    def __get_header_list(self):
        return self.table_frame.data.get_headers()

    def __get_data(self, col_selection):
        return self.table_frame.data.as_rows_id(col_selection)

    def __get_cols(
        self, col_idxs: list[int], class_col_idx: int
    ) -> tuple[list[list], list]:
        attr_cols = []
        for idx in col_idxs:
            if idx != class_col_idx:
                attr_cols.append(self.table_frame.data.cols[idx+1])
        return attr_cols, self.table_frame.data.cols[class_col_idx+1]
