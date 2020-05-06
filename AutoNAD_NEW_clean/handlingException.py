import tkinter as tk
from tkinter import messagebox
class PrintDialogError():
    def __init__(self): pass
    def show_error(self, title="Error", message=None):
        messagebox.showerror(title=title, message=message)
# class PrintDialog():
#     def __init__(self, title, message):
#         messagebox.showerror(title, message)
# if __name__ == "__main__":
#     x = 5
#     y = x+5
#
#     PrintDialog(title="show Error", message="Show jaaa")
#     z = y+5
#     print(x+y)