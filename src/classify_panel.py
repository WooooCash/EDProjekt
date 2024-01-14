import tkinter as tk
import csv
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename

from src.binary_vector import BinaryVectorizer
from src.col_choice_window import ColChoice, NewRow
from src.data import parse_ints
from src.preprocessing2 import plot_2d
from src.table_frame import Table


class ClassifyPanel(tk.Frame):
    def __init__(self, parent, table_frame: Table, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.table_frame = table_frame

        self.structure_label = tk.Label(self, width=30)
        self.structure_label.grid()

        self.cluster_button = tk.Button(
            self, text="Cluster", command=self.__cluster, background="#AAFFAA"
        )

        self.classify_button = tk.Button(
            self, text="Classify", command=self.__classify, background="#AAFFFF"
        )

        self.cluster_button.grid(sticky=tk.EW)
        self.attr_cols = []
        self.class_col = []
        self.binary_vectors = []
        self.col_mapping = {}
        self.class_col_idx = -1
        self.new_rows = []
        self.row = ""

    def __cluster(self):
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
        id_col, attr_cols, class_col = self.__get_cols(cols, class_col_idx)
        print("arg_header_idxs", arg_header_idxs)
        print("col_mapping", col_mapping)

        binary_vectorizer = BinaryVectorizer(rows_with_id, attr_cols, class_col, id_col)
        result_data = binary_vectorizer()
        self.__remove_rows(binary_vectorizer.removed_points)
        id_col, attr_cols, class_col = self.__get_cols(cols, class_col_idx)

        if len(attr_cols) == 2:
            vlines = [b.value for b in result_data if b.col == 0]
            hlines = [b.value for b in result_data if b.col == 1]
            plot_2d(attr_cols[0], attr_cols[1], class_col, lines=(vlines, hlines))

        new_rows = [[] for _ in range(len(id_col))]

        for i in range(len(id_col)):
            row = [col[i] for col in attr_cols]
            for bv in result_data:
                new_rows[i].append(bv.classify(row))
            new_rows[i].append(class_col[i])

        self.__write_to_file(new_rows)

        self.attr_cols = attr_cols
        self.class_col = class_col
        self.binary_vectors = result_data
        self.col_mapping = col_mapping
        self.class_col_idx = class_col_idx
        self.new_rows = new_rows


        self.classify_button.grid(sticky=tk.EW)


    def __classify(self):
        choice_window = NewRow(self)
        self.wait_window(choice_window)
        row = self.row.split(" ")
        parsed_row = parse_ints(row)
        if (len(parsed_row) != len(self.col_mapping)):
            print(f"Bad row length. Expected {len(self.col_mapping)}")
            return

        new_row = []
        for bv in self.binary_vectors:
            new_row.append(bv.classify(parsed_row))

        print("Bin vec:")
        print(new_row)
       
        for r in self.new_rows:
            if new_row == r[:-1]:
                cl = r[-1]
                print(f"Class is {cl}!")
                return
        # attr_row = [parsed_row[i] for i in self.col_mapping.values()]
        print("No class found")

        

    def __write_to_file(self, data: list[list]):
        fn = asksaveasfilename()

        headers = [f"bve{i}" for i in range(1, len(data))]
        headers.append("class")

        with open(fn, "w", newline="") as file:
            writer = csv.writer(file, delimiter=" ")
            writer.writerow(headers)
            for row in data:
                writer.writerow(row)

        print("Saved binary vector data to ", fn)

    def __get_header_list(self):
        return self.table_frame.data.get_headers()

    def __get_data(self, col_selection):
        return self.table_frame.data.as_rows_id(col_selection)

    def __get_cols(
        self, col_idxs: list[int], class_col_idx: int
    ) -> tuple[list, list[list], list]:
        attr_cols = []
        for idx in col_idxs:
            if idx != class_col_idx:
                attr_cols.append(self.table_frame.data.cols[idx + 1])

        id_col = self.table_frame.data.cols[0]
        return id_col, attr_cols, self.table_frame.data.cols[class_col_idx + 1]

    def __remove_rows(self, row_ids: list[int]):
        self.table_frame.remove_rows(row_ids)
