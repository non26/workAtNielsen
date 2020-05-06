import tkinter as tk
from tkinter import filedialog
import json
from json import JSONDecodeError
from .DataBase.service import Service
from .DataBase.configurations import pathConfigurations
# from PyNielsen.AutoNAD.DataBase.configurations import pathConfigurations
import threading
class Setting():
    def __init__(self, master):
        # super().__init__()
        self.master = master
        self.master.title("setting")
        self.master.geometry("800x350") #WxH
        # create variable
        self.rootNADMonthly = tk.StringVar()
        self.rootNADWeekly = tk.StringVar()
        self.trendFile = tk.StringVar()
        self.checkList = tk.StringVar()
        # show the previous setting at the Entry of setting
        # Frame Widget
        # rootNADMonthly Frame
        self.rootNADMonthly_labelFrame = tk.LabelFrame(self.master
                                                       , text="Root NAD Monthly Folder"
                                                       , borderwidth=1, width=500, height=50)
        self.rootNADMonthly_labelFrame.grid(row=0, rowspan=2, column=0, columnspan=3, padx=10, pady=10, stick="W")
        self.rootNADMonthly_frame = tk.Frame(self.rootNADMonthly_labelFrame, width=500, height=50, borderwidth=1)
        self.rootNADMonthly_frame.grid(row=0, rowspan=2, column=0, columnspan=3, stick="W")
        # rootNADWeekly Frame
        self.rootNADWeekly_labelFrame = tk.LabelFrame(self.master
                                                      , text="Root NAD Weekly Folder"
                                                      , borderwidth=1, width=500, height=50)
        self.rootNADWeekly_labelFrame.grid(row=2, rowspan=2, column=0, columnspan=3, padx=10, pady=10, stick="W")
        self.rootNADWeekly_frame = tk.Frame(self.rootNADWeekly_labelFrame, width=500, height=50, borderwidth=1)
        self.rootNADWeekly_frame.grid(row=2, rowspan=2, column=0, columnspan=3, stick="W")
        # trendCheck Frame
        self.trendCheck_labelFrame = tk.LabelFrame(self.master
                                                   , text="TrendCheck File"
                                                   , borderwidth=1, width=500, height=50)
        self.trendCheck_labelFrame.grid(row=4, rowspan=2, column=0, columnspan=3, stick="W", pady=10, padx=10)
        self.trendCheck_frame = tk.Frame(self.trendCheck_labelFrame, width=500, height=50, borderwidth=1)
        self.trendCheck_frame.grid(row=4, rowspan=2, column=0, columnspan=3, stick="W")
        # checkList Frame
        self.checkList_labelFrame = tk.LabelFrame(self.master
                                                  , text="Check List File"
                                                  , borderwidth=1, width=500, height=50)
        self.checkList_labelFrame.grid(row=6, rowspan=2, column=0, columnspan=3, sticky="W", pady=10, padx=10)
        self.checkList_frame = tk.Frame(self.checkList_labelFrame, width=500, height=50, borderwidth=1)
        self.checkList_frame.grid(row=6, column=0, columnspan=3, sticky="W")
        # stop making those widget have contracted size
        self.rootNADMonthly_labelFrame.grid_propagate(0)
        self.rootNADWeekly_labelFrame.grid_propagate(0)
        self.trendCheck_labelFrame.grid_propagate(0)
        self.checkList_labelFrame.grid_propagate(0)
        # assign value to each Entry
        # Button Widget
        # rootNADMonthly Button
        self.rootNADMonthly_button = tk.Button(self.rootNADMonthly_frame
                                               , text="select Root NAD Monthly Folder:"
                                               , command=self.open_rootNADMonthlyFolder)
        self.rootNADMonthly_button.grid(row=0, column=0, sticky="W")
        # rootNADWeekly Button
        self.rootNADWeekly_button = tk.Button(self.rootNADWeekly_frame
                                               , text="select Root NAD Weekly Folder:"
                                               , command=self.open_rootNADWeeklyFolder)
        self.rootNADWeekly_button.grid(row=0, column=0, sticky="W")
        # trendCheck Button
        self.trendCheck_button = tk.Button(self.trendCheck_frame
                                           , text="select TrendCheck File:"
                                           , command=self.open_trendCheckFile)
        self.trendCheck_button.grid(row=0, column=0, sticky="W")
        # checkList Button
        self.checkList_button = tk.Button(self.checkList_frame
                                          , text="select Check List File"
                                          , command=self.open_checkListFile)
        self.checkList_button.grid(row=0, column=0, sticky="W")
########
        # save Button
        threa1 = threading.Thread(target=self.save)
        self.saveSetting_button = tk.Button(self.master, text="save", command=threa1.start, width=10)
        # self.saveSetting_button = tk.Button(self.master, text="save", command=self.save, width=10)
        self.saveSetting_button.grid(row=8, column=1, columnspan=3)
########
        # Entry Widget
        # rootNADMonthly Entry
        self.rootNADMonthly_entry = tk.Entry(self.rootNADMonthly_frame
                                             , textvariable=self.rootNADMonthly, width=50)
        # self.rootNADMonthly_entry["width"] = 50
        self.rootNADMonthly_entry.grid(row=0, column=1, sticky='S', padx=10)
        # rootNADWeekly Entry
        self.rootNADWeekly_entry = tk.Entry(self.rootNADWeekly_frame
                                            , textvariable=self.rootNADWeekly, width=50)
        # self.rootNADWeekly_entry["width"] = 50
        self.rootNADWeekly_entry.grid(row=0, column=1, sticky='S', padx=10)
        # trendCheck Entry
        self.trendCheck_entry = tk.Entry(self.trendCheck_frame
                                         , textvariable=self.trendFile, width=50)
        # self.trendCheck_entry["width"] = 50
        self.trendCheck_entry.grid(row=0, column=1, padx=10)
        # checkList Entry
        self.checkList_entry = tk.Entry(self.checkList_frame
                                        , textvariable=self.checkList)
        self.checkList_entry["width"] = 50
        self.checkList_entry.grid(row=0, column=1, padx=10)
        # make the cursor can moving to the end of the Entry
        self.rootNADMonthly_entry.icursor(tk.END)
        self.rootNADMonthly_entry.icursor(tk.END)
        self.trendCheck_entry.icursor(tk.END)
        self.checkList_entry.icursor(tk.END)

        config = self.show_configuration()
        self.rootNADMonthly.set(config["rootNADMonthly"])
        self.rootNADWeekly.set(config["rootNADWeekly"])
        self.checkList.set(config["checkList"])
        self.trendFile.set(config["trendCheck"])

    def open_rootNADMonthlyFolder(self):
        rootNAD = filedialog.askdirectory(initialdir="C:", title = "select Monthly NAD Root")
        self.rootNADMonthly.set(rootNAD)
        self.rootNADMonthly_entry["width"] = len(rootNAD)

    def open_rootNADWeeklyFolder(self):
        rootNAD = filedialog.askdirectory(initialdir="C:", title = "select Weekly NAD Root")
        self.rootNADWeekly.set(rootNAD)
        self.rootNADWeekly_entry["width"] = len(rootNAD)

    def open_trendCheckFile(self):
        file = filedialog.askopenfilename(initialdir="C:", title = "select TrendCheck")
        self.trendFile.set(file)
        self.trendCheck_entry["width"]=len(file)

    def open_checkListFile(self):
        file = filedialog.askopenfilename(initialdir="C:", title = "select CheckList")
        self.checkList.set(file)
        self.checkList_entry["width"] = len(file)

    def save(self):
        print("saving")
        path = pathConfigurations
        element = {}
        with open(path + "\\" + "configFile.json", 'w') as infile:
            element["rootNADMonthly"] = self.rootNADMonthly.get()
            element["rootNADWeekly"] = self.rootNADWeekly.get()
            element["trendCheck"] = self.trendFile.get()
            element["checkList"] = self.checkList.get()
            json.dump(element, infile)
            storeService = Service.Service(pathCheckList=self.checkList.get())
            storeService.writing_service(value=storeService.finding_fromCheckList())
        print("finish saving")

    @staticmethod
    def show_configuration():
        path = pathConfigurations
        try:
            with open(path + "\\" + "configFile.json", 'r') as infile: # deal with this file when it doesn't exist
                config = json.load(infile)
                return config
        except JSONDecodeError:
            config = {"rootNADMonthly":'', "rootNADWeekly":''
                      , "trendCheck":'', "checkList":''}
            return config
    @staticmethod
    def reset_configuration():
        path = pathConfigurations
        element = {}
        with open(path + "\\" + "configFile.json", 'w') as infile:
            element["rootNADMonthly"] = ""
            element["rootNADWeekly"] = ""
            element["trendCheck"] = ""
            element["checkList"] = ""
            json.dump(element, infile, default={})


if __name__=="__main__":
    root = tk.Tk()
    window=Setting(root)
    print(window.show_configuration())
    root.mainloop()
