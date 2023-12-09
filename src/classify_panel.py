import tkinter as tk
from tkinter import messagebox

from src.col_choice_window import ColChoice
from src.table_frame import Table


class ClassifyPanel(tk.Frame):
    def __init__(self, parent, table_frame: Table, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.table_frame = table_frame

        self.structure_label = tk.Label(self, width=30)
        self.structure_label.grid()

        self.classify_button = tk.Button(
            self, text="Classify", command=self.__classify, background="#AAFFAA"
        )

        self.classify_button.grid(sticky=tk.EW)

    def __classify(self):
        cols = self.table_frame.get_selected_cols()
        if len(cols) < 3:
            messagebox.showerror("Error", "Must select at least 3 columns")
            return

        data_headers = self.__get_header_list()
        headers = {i: data_headers[i] for i in cols}
        classifier = tk.IntVar(self)
        choice_window = ColChoice(headers, classifier)
        self.wait_window(choice_window)
        class_col_idx = classifier.get()

        arg_header_idxs = [
            header_key for header_key in headers.keys() if header_key != class_col_idx
        ]
        rows_with_id, col_mapping = self.__get_data(arg_header_idxs)
        print("arg_header_idxs", arg_header_idxs)
        print("col_mapping", col_mapping)

    def __get_header_list(self):
        return self.table_frame.data.get_headers()

    def __get_data(self, col_selection):
        return self.table_frame.data.as_rows_id(col_selection)

    def __get_col(self, idx):
        col = self.table_frame.data.cols[idx]
        header = self.table_frame.data.headers[idx]
        return col, header
