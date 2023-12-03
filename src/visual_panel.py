import tkinter as tk

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
