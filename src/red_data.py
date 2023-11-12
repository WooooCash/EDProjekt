import tkinter as tk
from tkinter import filedialog

def otworz_plik():
    sciezka_pliku = filedialog.askopenfilename()

    if sciezka_pliku:
        with open(sciezka_pliku, 'r') as plik:
            zawartosc = plik.read()
            print(zawartosc)


root = tk.Tk()

przycisk = tk.Button(root, text="Otwórz plik", command=otworz_plik)
przycisk.pack()

root.mainloop()

