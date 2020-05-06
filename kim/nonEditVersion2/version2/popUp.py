import tkinter as tk
from tkinter import messagebox
# https://stackoverflow.com/questions/2963263/how-can-i-create-a-simple-message-box-in-python
def alert_popUp(title, message, service, path=""):
    """Generate a pop-up window for special messages."""
    root = tk.Tk()
    root.title(title)
    root.wm_withdraw()
    m = message
    m += '\n'
    m += path
    messagebox.showinfo(title=f"{title}.", message=f"{message}: {service}.")
if __name__ == "__main__":
    alert_popUp("Title goes here..", "Hello World!", "A path or second message can go here..")
    super()