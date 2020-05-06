from ..DataBase.configurations import *
import json
import os
# from ..BackEnd_Weekly import weekly_class as wc
from ..BackEnd_Weekly import weekly_class_revamped as wc
from .. import searchingword as sw
# from ..progressBar import ProgressBar
# from tkinter import TclError
import tkinter as tk
from ..FrontEnd_Weekly import conclusionSection_Weekly as ccw
import datetime
class WeekWindow():
    """This class is used to input the weekly information section"""
    def __init__(self, master):
        self.master = master
        self.nadVar = tk.StringVar()
        self.trendVar = tk.StringVar()
        self.checkListVar = tk.StringVar()
        self.weekthVar = tk.StringVar()
        self.serviceVar = tk.StringVar()

        # # Label
        self.rootFolder = tk.Label(self.master, text="Root NAD Weekly Folder: ").grid(row=0, column=0, padx=(10, 5),
                                                                                      sticky='w')
        self.trendFile = tk.Label(self.master, text="Trend Check File: ").grid(row=1, column=0, padx=(10, 5),
                                                                               sticky='w')
        self.checkList = tk.Label(self.master, text="Check List File: ").grid(row=2, column=0, padx=(10, 5)
                                                                              , sticky='w')
        self.weekth = tk.Label(self.master, text="Weekth/year: ").grid(row=3, column=0, padx=(10, 5), sticky='w')
        note = "NOTE: specify in the form of minWeekth-maxWeekth-year Ex. 43-46-2019"
        tk.Label(self.master, text=note).grid(row=4, column=0, columnspan=6, padx=(10, 5), pady=5,sticky='w')
        self.chooseService_entry = tk.Label(self.master, text="Choose Service: ").grid(row=5, column=0, padx=(10, 5)
                                                                                       , sticky='w')
        # # Entry
        # Entry---nad
        self.nad = tk.Entry(self.master, textvariable=self.nadVar, width=40, state="readonly")
        self.nad.grid(row=0, column=1, columnspan=5)
        # Entry---trend
        self.trend = tk.Entry(self.master, textvariable=self.trendVar, width=40, state="readonly")
        self.trend.grid(row=1, column=1, columnspan=5)
        # Entry---checkList
        self.checkList = tk.Entry(self.master, textvariable=self.checkListVar, width=40, state="readonly")
        self.checkList.grid(row=2, column=1, columnspan=5)
        # Entry---weekth
        self.weekth = tk.Entry(self.master, textvariable=self.weekthVar, width=40)
        self.weekth.grid(row=3, column=1, columnspan=5)
        # Entry---choose service
        self.chooseService_entry = tk.Entry(self.master, textvariable=self.serviceVar, width=40)
        self.chooseService_entry.grid(row=5, column=1, columnspan=5)
        sw.ServiceAutoCompleteEntry(master=self.chooseService_entry, mastervariable=self.serviceVar
                                    , parentMaster=self.master, row=6, column=1)

        # # button
        self.run_button = tk.Button(self.master, text="RUN", command=self.running)
        self.run_button.grid(row=6, column=1, columnspan=5, sticky='WE')

        self.setWeeklyDetail()
        self.conclude = ccw.conclude(self.master)
        ccw.openLogButton(self.master)
        # # progressBar
        # # MenuOption
        # Menuoption---service

    def running(self):
        """This method is running when the user press the RUN button"""
        # try:
            # self.pb.restartWidget()
        # except (TclError, Exception): pass
        del self.conclude.runningDate
        del self.conclude.totalFail
        del self.conclude.totalFiles
        del self.conclude.totalTime
        self.conclude.runningDate = datetime.datetime.now().strftime("%c")
        # self.pb = ProgressBar(self.master, gridrow=7, gridcolumn=1, gridColumnSpan=5)
        weekth = self.weekthVar.get()
        service = self.serviceVar.get()
        week = wc.Weekly(selectedService=service, weekth=weekth, conclude=self.conclude)
        week.mainCompare()
    def setWeeklyDetail(self):
        path = pathConfigurations
        with open(path + "\\" + "configFile.json") as infile:
            content = json.load(infile)
            self.nadVar.set(os.path.basename(content["rootNADWeekly"]))
            self.trendVar.set(os.path.basename(content["trendCheck"]))
            self.checkListVar.set(os.path.basename(content["checkList"]))
            self.weekthVar.set(wc.findWeek(fileTrendPath=os.path.basename(content["trendCheck"])))

