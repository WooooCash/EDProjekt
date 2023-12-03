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

        data_headers = self.__get_header_list()
        headers = {i: data_headers[i] for i in cols}
        classifier = tk.IntVar(self)
        choice_window = ColChoice(headers, classifier)
        self.wait_window(choice_window)
        print(
            f"CHOSEN CLASSIFIER: {classifier.get()} | {data_headers[classifier.get()]}"
        )

    def __get_header_list(self):
        return self.table_frame.data.headers
