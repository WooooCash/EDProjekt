import tkinter as tk
from tkinter import ttk
from src.panel import LoadPanel
from src.op_panel import OperationPanel
from src.table_frame import Table

class MainPanel(ttk.Notebook):
    def __init__(self, parent, table_frame: Table, *args, **kwargs):
        ttk.Notebook.__init__(self, parent, *args, **kwargs)

        load_panel = LoadPanel(self, table_frame, *args, **kwargs)
        op_panel = OperationPanel(self, table_frame, *args, **kwargs)
        self.add(load_panel, text="Load")
        self.add(op_panel, text="Ops")

