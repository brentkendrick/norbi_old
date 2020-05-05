# Import required modules
import sys, os, math, warnings
from tkinter import Tk, filedialog
from tkinter.filedialog import askopenfilename, askopenfilenames


def select_file():
    Tk().withdraw()

    ftypes = [("xls or xlsx files", "*.xls *.xlsx")]

    data_file = str(askopenfilename(filetypes=ftypes, title="Choose the xlsx file."))

    return data_file


import tkinter as tk
from tkinter import filedialog

def select_files2():
    root = tk.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    files = filedialog.askopenfilename(multiple=True) 
    # %gui tk
    var = root.tk.splitlist(files)
    filePaths = []
    for f in var:
        filePaths.append(f)
    return filePaths
