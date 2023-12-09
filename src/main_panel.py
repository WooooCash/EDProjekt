import tkinter as tk
from tkinter import ttk
from src.classify_panel import ClassifyPanel
from src.load_panel import LoadPanel
from src.op_panel import OperationPanel
from src.table_frame import Table
from src.visual_panel import VisualPanel


class MainPanel(ttk.Notebook):
    def __init__(self, parent, table_frame: Table, *args, **kwargs):
        ttk.Notebook.__init__(self, parent, *args, **kwargs)

        load_panel = LoadPanel(self, table_frame, *args, **kwargs)
        op_panel = OperationPanel(self, table_frame, *args, **kwargs)
        visual_panel = VisualPanel(self, table_frame, *args, **kwargs)
        classify_panel = ClassifyPanel(self, table_frame, *args, **kwargs)
        self.add(load_panel, text="Load")
        self.add(op_panel, text="Ops")
        self.add(visual_panel, text="Visual")
        self.add(classify_panel, text="Classify")
