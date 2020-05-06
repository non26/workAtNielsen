import tkinter as tk
from tkinter import messagebox
# import tkinter
# https://stackoverflow.com/questions/2963263/how-can-i-create-a-simple-message-box-in-python
def alert_popUp(title, message):
    """Generate a pop-up window for special messages."""

    root = tk.Tk()
    root.title(title)
    root.wm_withdraw()
    w = 400     # popup window width
    h = 200     # popup window height
    # sw = root.winfo_screenwidth()
    # sh = root.winfo_screenheight()
    # x = (sw - w)/2
    # y = (sh - h)/2
    # root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message
    m += '\n'
    # w = tk.Label(root, text=m, width=120, height=10)
    # w.pack()
    # b = tk.Button(root, text="OK", command=root.destroy, width=10)
    # b.pack()
    w = messagebox.showinfo(title=f"{title}.", message=f"{message}.")
    # root.mainloop()
if __name__ == "__main__":
    alert_popUp("Title goes here..", "Hello World!")