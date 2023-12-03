import tkinter as tk
from tkinter import messagebox


class ColChoice(tk.Toplevel):
    def __init__(self, headers: dict[int, str], classifier: tk.IntVar):
        super().__init__()
        self.title(f"TK_ED - classifier column choice")
        label = tk.Label(self, text="Choose class column")
        headers.values()
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
