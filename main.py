import tkinter as tk

# from app.image_frame import ImageFrame
from src.panel import Panel


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # self.image_frame = ImageFrame(self, width=700, height=700)
        self.panel = Panel(self)

        self.panel.grid(row=0, column=0)
        # self.image_frame.grid(row=0, column=1)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("TK_Grafika")
    app = MainApplication(root)
    app.pack(side="top", fill="both", expand=True)
    root.geometry('500x400')
    root.mainloop()
