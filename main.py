import tkinter as tk
from src.main_panel import MainPanel

from src.table_frame import Table


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.table_frame = Table(self)
        self.panel = MainPanel(self, self.table_frame)

        self.panel.grid(row=0, column=0)
        self.table_frame.grid(row=0, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("TK_ED")
    app = MainApplication(root)
    app.pack(side="top", fill="both", expand=True)
    # root.geometry('500x400')
    root.mainloop()
