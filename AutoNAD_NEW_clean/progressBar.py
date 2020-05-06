from tkinter import ttk
import tkinter as tk

import time
class ProgressBar():
    def __init__(self, master, gridrow, gridcolumn, gridRowSpan=None, gridColumnSpan=None):
        """
        :param master:
        :param gridrow:
        :param gridcolumn:
        # :param option: can be
        """
        self.master = master
        self.value = 0
        self.progressWidget = ttk.Progressbar(self.master, orient=tk.HORIZONTAL
                                         , mode='determinate')
        self.progressWidget.grid(row=gridrow, column=gridcolumn
                                 , rowspan=gridRowSpan, columnspan=gridColumnSpan, sticky="WE")

    def increaseValue(self, increase):
        self.value += increase
        self.progressWidget["value"] = self.value
        # time.sleep(0.5)
        self.master.update_idletasks()
    def restartWidget(self):
        # self.progressWidget.destroy()
        self.progressWidget.stop()
        self.progressWidget.configure(mode="indeterminate", value=0)
        self.progressWidget.configure(mode="determinate", value=0, maximum=0)
if __name__ == "__main__":
    root = tk.Tk()
    increase_button = tk.Button(root, text="ProgressBar")
    increase_button.grid(row=0, column=0)
    restart_button = tk.Button(root, text="restart")
    restart_button.grid(row=1, column=0)
    pb = ProgressBar(master=root, gridrow=0, gridcolumn=1)
    pb.progressWidget["maximum"] = 49
    restart_button["command"] = pb.restartWidget
    increase_button["command"] = lambda x=7: pb.increaseValue(x)
    # for i in range(7):
    #     pb.increaseValue(7)
        # time.sleep(1)
    root.update_idletasks()
    root.mainloop()