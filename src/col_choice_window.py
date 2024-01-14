import tkinter as tk
from tkinter import messagebox


class ColChoice(tk.Toplevel):
    def __init__(self, headers: dict[int, str], classifier: tk.IntVar):
        super().__init__()
        self.title(f"TK_ED - classifier column choice")
        label = tk.Label(self, text="Choose class column")
        column_options = self.__generate_options(classifier, headers)
        confirm_button = tk.Button(self, text="Confirm", command=self.destroy)

        label.grid()
        for option in column_options:
            option.grid(sticky=tk.EW)

        confirm_button.grid()

    def __generate_options(self, classifier, headers: dict[int, str]):
        options_list = []
        for idx, header in headers.items():
            options_list.append(
                tk.Radiobutton(self, text=header, variable=classifier, value=idx)
            )

        return options_list


class NewRow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.title(f"TK_ED - New Row")
        label = tk.Label(self, text="Enter new row", width=50)
        self.row_entry = tk.Entry(self)
        self.confirm_button = tk.Button(self, text="Confirm", command=self.confirm)

        label.grid()
        self.row_entry.grid(sticky=tk.EW)
        self.confirm_button.grid()

    def confirm(self):
        self.parent.row = self.row_entry.get()
        self.destroy()
