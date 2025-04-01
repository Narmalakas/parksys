import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("300x300")
root.resizable(False, False)


main_frame = ttk.Frame(root, padding="3 3 12 12")
main_frame.grid(column=0, row=0)

app = ttk.Frame(main_frame)
app.grid(column=1, row=0)

MainWindow = ttk.Frame(main_frame)
MainWindow.grid(column=2, row=0)

